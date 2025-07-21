#!/usr/bin/env python3
"""
PySpark Environment Test Script
Tests PySpark installation and basic functionality for HVAC Assistant project.
"""

import sys
import os
from datetime import datetime

def test_python_version():
    """Test Python version compatibility."""
    print("=" * 60)
    print("PYTHON VERSION TEST")
    print("=" * 60)
    
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor == 10:
        print("✅ Python 3.10.x detected - Compatible!")
        return True
    else:
        print("❌ Python 3.10.x required for this project")
        return False

def test_environment_variables():
    """Test required environment variables."""
    print("\n" + "=" * 60)
    print("ENVIRONMENT VARIABLES TEST")
    print("=" * 60)
    
    variables = {
        'JAVA_HOME': os.getenv('JAVA_HOME'),
        'HADOOP_HOME': os.getenv('HADOOP_HOME'),
        'PATH': os.getenv('PATH')
    }
    
    success = True
    
    for var, value in variables.items():
        if value:
            if var == 'PATH':
                print(f"✅ {var}: Set (length: {len(value)} chars)")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")
            success = False
    
    return success

def test_pyspark_import():
    """Test PySpark import and version."""
    print("\n" + "=" * 60)
    print("PYSPARK IMPORT TEST")
    print("=" * 60)
    
    try:
        import pyspark
        print(f"✅ PySpark imported successfully")
        print(f"✅ PySpark Version: {pyspark.__version__}")
        
        if pyspark.__version__.startswith('3.5'):
            print("✅ PySpark 3.5.x detected - Compatible!")
            return True
        else:
            print("⚠️  Expected PySpark 3.5.x, but this version should work")
            return True
            
    except ImportError as e:
        print(f"❌ Failed to import PySpark: {e}")
        return False

def test_spark_session():
    """Test Spark session creation and basic operations."""
    print("\n" + "=" * 60)
    print("SPARK SESSION TEST")
    print("=" * 60)
    
    try:
        from pyspark.sql import SparkSession
        
        # Create Spark session with HVAC Assistant configuration
        spark = SparkSession.builder \
            .appName("HVAC-Assistant-Test") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .getOrCreate()
        
        print("✅ Spark session created successfully")
        print(f"✅ Spark Version: {spark.version}")
        print(f"✅ Application Name: {spark.sparkContext.appName}")
        
        # Test basic DataFrame operations
        print("\n📊 Testing DataFrame operations...")
        
        # Create test data (HVAC equipment sample)
        test_data = [
            ("Carrier", "58MCA", "Gas Furnace", 80000),
            ("Goodman", "GMH95", "Gas Furnace", 95000),
            ("Trane", "XR95", "Gas Furnace", 100000),
            ("Lennox", "SLP98V", "Gas Furnace", 98000)
        ]
        
        columns = ["manufacturer", "model", "type", "btu_rating"]
        
        df = spark.createDataFrame(test_data, columns)
        
        print("✅ Test DataFrame created")
        print(f"✅ Row count: {df.count()}")
        
        print("\n📋 Sample data:")
        df.show()
        
        # Test aggregation (typical for HVAC analysis)
        print("📊 Testing aggregation (average BTU by manufacturer):")
        avg_btu = df.groupBy("manufacturer").avg("btu_rating")
        avg_btu.show()
        
        print("✅ All DataFrame operations successful!")
        
        # Clean up
        spark.stop()
        print("✅ Spark session stopped cleanly")
        
        return True
        
    except Exception as e:
        print(f"❌ Spark session test failed: {e}")
        try:
            spark.stop()
        except:
            pass
        return False

def test_java_integration():
    """Test Java integration with PySpark."""
    print("\n" + "=" * 60)
    print("JAVA INTEGRATION TEST")
    print("=" * 60)
    
    try:
        from pyspark import SparkContext
        
        # This will fail if Java is not properly configured
        sc = SparkContext.getOrCreate()
        
        print("✅ Java integration working")
        print(f"✅ Spark Context: {sc}")
        print(f"✅ Master: {sc.master}")
        
        # Test RDD operations (lower level than DataFrames)
        test_rdd = sc.parallelize([1, 2, 3, 4, 5])
        result = test_rdd.map(lambda x: x * 2).collect()
        
        print(f"✅ RDD operations successful: {result}")
        
        sc.stop()
        return True
        
    except Exception as e:
        print(f"❌ Java integration test failed: {e}")
        return False

def run_all_tests():
    """Run all PySpark tests."""
    print("🔧 PYSPARK ENVIRONMENT TEST FOR HVAC ASSISTANT")
    print(f"🕐 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"💻 Operating System: {os.name}")
    
    tests = [
        ("Python Version", test_python_version),
        ("Environment Variables", test_environment_variables),
        ("PySpark Import", test_pyspark_import),
        ("Java Integration", test_java_integration),
        ("Spark Session", test_spark_session)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! PySpark environment is ready for HVAC Assistant development.")
    else:
        print("⚠️  Some tests failed. Check the output above for troubleshooting guidance.")
        print("💡 Tip: Ensure your virtual environment is activated and WSL environment variables are loaded.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)