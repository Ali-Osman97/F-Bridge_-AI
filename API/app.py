from flask import Flask, request, jsonify, render_template
from google import genai 
from dotenv import load_dotenv 
import os


load_dotenv()



app=Flask(__name__) # Implement rate limiting (Flask-Limiter) & Force HTTPS in production

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY") # Don't forget to add key validation and graceful degradation
client = genai.Client(api_key=GOOGLE_API_KEY)




@app.route("/api", methods=["GET"])
def Get_form():
    return render_template("form.html")


@app.route("/api/Strategy", methods=["POST"])
def get_battle_plan_strategy():
    
    user_struggle_text=request.form.get("user_struggle") # Implement input sanitization and length limits

    if not user_struggle_text:
         return render_template('form.html', error="Missing 'user_struggle' in the form.")
    

    prompt=f""" 
                You are an accountability coach. A user is struggling with: '{user_struggle_text}'.  
                Generate a 3-step, actionable 'Battle Plan' for them.  
                The tone should be supportive but firm. Return only the 3 steps. 
            """ 

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )
        battle_plan = response.text
        return render_template('form.html', battle_plan=battle_plan)

    
    except Exception as e:
        return render_template('form.html', error=str(e))




if __name__ == "__main__":
    app.run(debug=True) $ Use Production WSGI server (Gunicorn, uWSGI)


