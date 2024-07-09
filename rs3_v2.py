import os
import findspark
findspark.init()

# Set the environment variables for PySpark
os.environ['PYSPARK_PYTHON'] = 'C:\\Users\\enman\\Downloads\\UESAN\\rs3\\venv\\Scripts\\python.exe'
os.environ['PYSPARK_DRIVER_PYTHON'] = 'C:\\Users\\enman\\Downloads\\UESAN\\rs3\\venv\\Scripts\\python.exe'
os.environ['HADOOP_HOME'] = 'C:\\path\\to\\hadoop'
os.environ['PATH'] += os.pathsep + os.path.join(os.environ['HADOOP_HOME'], 'bin')

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SimpleJob") \
    .config("spark.executor.memory", "4g") \
    .config("spark.driver.memory", "4g") \
    .config("spark.driver.maxResultSize", "2g") \
    .getOrCreate()

data = [("John", "Smith"), ("Anna", "Rose"), ("Robert", "Williams")]
columns = ["FirstName", "LastName"]

df = spark.createDataFrame(data, columns)
df.show()

spark.stop()
