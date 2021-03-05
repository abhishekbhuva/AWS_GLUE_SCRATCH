from awsglue.context import GlueContext
from pyspark.context import SparkContext
from awsglue.job import job
import sys
from awsglue.utils import getResolvedOptions

#Glue Parametes
glueContext = GlueContext(SparkContext.getOrCreate()) #For spark Context
glueJob = Job(glueContext)
args= getResolvedOptions(sys.argv,['Name of the Job']) #JobName for Glue Job as a Argument

glueJob.init(args['Name of the Job'],args)
sparkSession = glueContext.sparksession  #Since it is a Glue job it will take Sparksession from GLue it slf

##ETL Code/Connections

spark_df = sparkSession.read.format("jdbc")\
    .options("url","jdbc:....") \ #JDBC database connection
    .option("driver","com.sql.jdbc.....") \ #JDBC Driver Details
    .option("dbtable","name of database") \ #Database Table name
    .option("user","username") \ #Username credential
    .option("password","password") \ #Password of that user
    .load()

print("Count of users in table",spark_df.count()) #This will give count of table in Database
print("Schema of the Table: ",spark_df.printSchema()) #This will print schema of that table

#Convert spark DF to Dynamic DF and writes to S3
dynamic_df = DynamicFrame.fromDF(
    spark_df,
    glueContext,
    "convert_ctx"
)

#Write Data to S3 in Parquet Format
glueContext.write_dynamic_frame.from_options(
    frame = dynamic_df,
    connection_type = "s3",
    connection_options = {"path:":"s3path"},
    format= "parquet",
    transformation_ctx = "transformation_ctx"
)
glueJob.commit()
