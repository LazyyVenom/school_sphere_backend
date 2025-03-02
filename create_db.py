import pymysql

# Connect to MySQL server (XAMPP default settings)
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    port=3306
)

try:
    with connection.cursor() as cursor:
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS school_sphere")
        print("Database 'school_sphere' created or already exists")
        
        # Select the database
        cursor.execute("USE school_sphere")
        print("Using database 'school_sphere'")
        
finally:
    connection.close()

print("Database setup complete!")

# Now you can run your FastAPI app, which will create the tables
print("You can now run your FastAPI app to create the tables.")
