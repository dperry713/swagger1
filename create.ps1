# Define the base directory
$baseDir = "factory_management_api"

# Define the subdirectories and files
$subDirs = @(
    "app",
    "app\__init__.py",
    "app\models.py",
    "app\routes.py",
    "migrations", # This will be auto-generated after initializing the database
    "config.py",
    "requirements.txt",
    "run.py",
    "README.md"
)

# Create the base directory
New-Item -ItemType Directory -Path $baseDir

# Create the subdirectories and files
foreach ($item in $subDirs) {
    if ($item -like "*.*") {
        New-Item -ItemType File -Path "$baseDir\$item"
    } else {
        New-Item -ItemType Directory -Path "$baseDir\$item"
    }
}

Write-Host "Directory structure created successfully."
