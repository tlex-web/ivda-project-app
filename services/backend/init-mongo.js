// MongoDB initialization script
// This script will be executed when MongoDB container starts

// Switch to the companies database
db = db.getSiblingDB("companies");

// Create the companiesdb collection and insert data from main_company.json
// The data will be imported via Docker volume mount
