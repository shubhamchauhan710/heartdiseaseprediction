# Vercel Deployment Guide

## Prerequisites
- Vercel account (https://vercel.com)
- Git repository pushed to GitHub

## Deployment Options

### Option 1: Deploy Streamlit App Directly (Recommended)
Your Streamlit app can be deployed to Vercel using the Streamlit configuration.

1. **Connect your GitHub repository to Vercel**
   - Go to https://vercel.com/new
   - Import your GitHub repository
   - Select "Import Project"

2. **Configure Vercel Settings**
   - Framework: Python
   - Build Command: `pip install -r requirements.txt`
   - Output Directory: Leave default
   - Environment Variables: Add if needed

3. **Deploy**
   - Click "Deploy"
   - Wait for build to complete

### Option 2: Use API Endpoint (Alternative)
The `/api` folder contains a serverless function that provides an API endpoint for predictions.

**API Endpoint:** `POST /api/index`

**Request Body:**
```json
{
  "features": [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
}
```

**Example Features (13 values):**
- age: Patient's age
- sex: Sex (0=female, 1=male)
- cp: Chest pain type
- trestbps: Resting blood pressure
- chol: Serum cholesterol
- fbs: Fasting blood sugar
- restecg: Resting electrocardiographic results
- thalach: Maximum heart rate achieved
- exang: Exercise induced angina
- oldpeak: ST depression
- slope: Slope of ST segment
- ca: Number of major vessels
- thal: Thalassemia

**Response:**
```json
{
  "prediction": 0 or 1,
  "result": "The Person does not have a Heart Disease" or "The Person has Heart Disease",
  "probability": 0.0 or 1.0
}
```

## Files Created for Vercel

- **vercel.json** - Vercel configuration file
- **requirements.txt** - Python dependencies
- **api/index.py** - Serverless API function
- **.gitignore** - Git ignore file
- **streamlit.app.toml** - Streamlit configuration

## Troubleshooting

### Model File Not Found
Ensure `trained_model.sav` is committed to your Git repository.

### Build Fails
- Check that all dependencies in `requirements.txt` are compatible
- Ensure Python version is 3.8 or higher
- Check Vercel logs for detailed error messages

### Deployment Takes Too Long
The first deployment may take longer. Subsequent deployments should be faster due to caching.

## Post-Deployment

- Test your API endpoint using curl or Postman
- Monitor performance in Vercel dashboard
- Set up analytics and error tracking if needed

## Environment Variables (Optional)

Add to Vercel dashboard if needed:
- `PYTHONUNBUFFERED=1` (already set in vercel.json)
