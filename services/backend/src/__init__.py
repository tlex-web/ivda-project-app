from flask import Flask, request
from flask_cors import CORS
from flask_restx import Resource, Api
from flask_pymongo import PyMongo
from pymongo.collection import Collection
from .model import Company

# Configure Flask & Flask-PyMongo:
app = Flask(__name__)
# allow access from any frontend
cors = CORS()
cors.init_app(app, resources={r"*": {"origins": "*"}})
# add your mongodb URI
import os

app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://mongodb:27017/companies")
pymongo = PyMongo(app)
# Get a reference to the companies collection.
companies: Collection = pymongo.db.companiesdb
api = Api(app)


class CompaniesList(Resource):
    def get(self, args=None):
        # retrieve the arguments and convert to a dict
        args = request.args.to_dict()
        # If the user specified category is "All" we retrieve all companies
        if args.get("category") == "All":
            cursor = companies.find()
        # In any other case, we only return the companies where the category applies
        else:
            cursor = companies.find(args)
        # we return all companies as json
        return [Company(**doc).to_json() for doc in cursor]


class Companies(Resource):

    def get(self, id):
        import pandas as pd
        from statsmodels.tsa.ar_model import AutoReg

        # search for the company by ID
        cursor = companies.find_one_or_404({"id": id})
        company = Company(**cursor)
        # retrieve args
        args = request.args.to_dict()
        # retrieve the profit
        profit = company.profit
        # add to df
        profit_df = pd.DataFrame(profit).iloc[::-1]
        if args["algorithm"] == "random":
            # retrieve the profit value from 2021
            prediction_value = int(profit_df["value"].iloc[-1])
            # add the value to profit list at position 0
            company.profit.insert(0, {"year": 2022, "value": prediction_value})
        elif args["algorithm"] == "regression":
            # create model
            model_ag = AutoReg(
                endog=profit_df["value"],
                lags=1,
                trend="c",
                seasonal=False,
                exog=None,
                hold_back=None,
                period=None,
                missing="none",
            )
            # train the model
            fit_ag = model_ag.fit()
            # predict for 2022 based on the profit data
            prediction_value = fit_ag.predict(
                start=len(profit_df), end=len(profit_df), dynamic=False
            ).values[0]
            # add the value to profit list at position 0
            company.profit.insert(0, {"year": 2022, "value": prediction_value})
        return company.to_json()


class CompanyPoem(Resource):
    def get(self, id):
        company = None
        try:
            print(f"Fetching poem for company ID: {id}")

            # Get company data first
            cursor = companies.find_one_or_404({"id": id})
            company = Company(**cursor)
            print(f"Found company: {company.name}")

            # Import the GroqClient here to avoid import issues
            from .llm.groq_llm import GroqClient
            import os

            # Initialize Groq client and generate poem
            groq_client = GroqClient()
            prompt_path = os.path.join(
                os.path.dirname(__file__), "llm", "prompts", "groq_api_poem.json"
            )

            print(f"Using prompt file: {prompt_path}")
            print(f"Prompt file exists: {os.path.exists(prompt_path)}")

            poem = groq_client.generate_poem(company.name, prompt_path)
            print(f"Generated poem: {poem[:100]}...")

            return {"poem": poem}

        except FileNotFoundError as e:
            error_msg = f"Company with ID {id} not found"
            print(f"Error: {error_msg}")
            return {"error": error_msg, "poem": error_msg}, 404

        except Exception as e:
            error_msg = f"Failed to generate poem: {str(e)}"
            company_name = company.name if company else f"company ID {id}"
            poem_msg = (
                f"Sorry, couldn't generate a poem for {company_name} at the moment."
            )
            print(f"Error: {error_msg}")
            return {"error": error_msg, "poem": poem_msg}, 500


class CompanyInfo(Resource):
    def get(self, id):
        company = None
        try:
            print(f"Fetching company info for company ID: {id}")

            # Get company data first
            cursor = companies.find_one_or_404({"id": id})
            company = Company(**cursor)
            print(f"Found company: {company.name}")

            # Import the GroqClient here to avoid import issues
            from .llm.groq_llm import GroqClient
            import os

            # Initialize Groq client and generate company info
            groq_client = GroqClient()
            prompt_path = os.path.join(
                os.path.dirname(__file__),
                "llm",
                "prompts",
                "groq_api_additional_information.json",
            )

            print(f"Using prompt file: {prompt_path}")
            print(f"Prompt file exists: {os.path.exists(prompt_path)}")

            company_info = groq_client.generate_company_info(company.name, prompt_path)
            print(f"Generated company info: {company_info[:100]}...")

            return {"company_info": company_info}

        except FileNotFoundError as e:
            error_msg = f"Company with ID {id} not found"
            print(f"Error: {error_msg}")
            return {"error": error_msg, "company_info": error_msg}, 404

        except Exception as e:
            error_msg = f"Failed to generate company info: {str(e)}"
            company_name = company.name if company else f"company ID {id}"
            info_msg = f"Sorry, couldn't generate company information for {company_name} at the moment."
            print(f"Error: {error_msg}")
            return {"error": error_msg, "company_info": info_msg}, 500


class TestPoem(Resource):
    def get(self):
        return {"message": "Poem API is working!", "test": True}


class TestCompanyInfo(Resource):
    def get(self):
        return {"message": "Company Info API is working!", "test": True}


# Register API resources
api.add_resource(CompaniesList, "/companies")
api.add_resource(Companies, "/companies/<int:id>")
api.add_resource(CompanyPoem, "/companies/<int:id>/poem")
api.add_resource(CompanyInfo, "/companies/<int:id>/info")
api.add_resource(TestPoem, "/test/poem")
api.add_resource(TestCompanyInfo, "/test/info")

print("🚀 All API resources registered successfully!")
print("📋 Registered endpoints:")
print("   - /companies")
print("   - /companies/<int:id>")
print("   - /companies/<int:id>/poem")
print("   - /companies/<int:id>/info")
print("   - /test/poem")
print("   - /test/info")
