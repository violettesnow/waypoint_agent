import 'dotenv/config';
import { MongoClient } from 'mongodb';
import { GoogleGenAI } from '@google/genai';
import express from 'express';

const app = express();
app.use(express.json());

// 1. Database Connection
// ⚠️ Replace YOUR_ACTUAL_PASSWORD with the one you just verified in MongoDB Atlas
const uri = "mongodb+srv://aivibelab:WAYpoint2026devpost@waypoint.n6dky2y.mongodb.net/?appName=WayPoint";
const mongoClient = new MongoClient(uri);
let db;

async function connectDB() {
    try {
        await mongoClient.connect();
        db = mongoClient.db("waypoint_db");
        console.log("✅ Connected to MongoDB");
    } catch (err) {
        console.error("❌ MongoDB Connection Error:", err);
    }
}
connectDB();

// 2. AI Setup
// This will automatically pull your GEMINI_API_KEY from the .env file
const ai = new GoogleGenAI({});

// 3. API Route
app.post('/api/reports/google-ingest', async (req, res) => {
    try {
        const { rawText, latitude, longitude } = req.body;

        // Call Gemini to validate and structure the report
        const response = await ai.models.generateContent({
            model: 'gemini-2.5-flash',
            contents: `Analyze this wildlife report: "${rawText}". 
                       Return strictly JSON with: category (corridor_blockage, sighting, or habitat_loss) and cleanedDetails.`
        });
        
        // Clean the response just in case Gemini adds markdown blocks like ```json
        const rawJson = response.text.replace(/```json\n?|```/g, '');
        const agentResult = JSON.parse(rawJson);

        // Create the report object
        const newReport = {
            reportType: agentResult.category,
            details: agentResult.cleanedDetails,
            location: { type: "Point", coordinates: [parseFloat(longitude), parseFloat(latitude)] },
            timestamp: new Date()
        };

        // Save to MongoDB
        await db.collection('reports').insertOne(newReport);
        console.log("💾 Saved to MongoDB");

        return res.status(201).json({ success: true, report: newReport });
    } catch (error) {
        console.error("❌ Error processing report:", error);
        return res.status(500).json({ error: error.message });
    }
});

app.listen(5000, () => console.log("🚀 WayPoint Ingestion Node active on port 5000"));