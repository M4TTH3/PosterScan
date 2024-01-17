import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';
import { NextResponse } from 'next/server'

export async function POST(req: NextApiRequest, res: NextApiResponse) {

    if (req.method != 'POST') {
        res.status(405).json({message: 'Only POST requests allowed'});
    }
    const chunks = [];
    for await (const chunk of req.body) {
        chunks.push(chunk);
    }

    const bodyString = Buffer.concat(chunks).toString('utf-8');

    const image = JSON.parse(bodyString);

    console.log("Parsed image: ", image);

    const scanPosterResponse = await axios.post('http://localhost:5000/api/scanposter', { image: image });
    console.log(scanPosterResponse);
    try {
        

        NextResponse.json({contents: contents});
    } 
    catch (error) {
        console.error('Error processing image', error);
        res.status(500).json({message: 'Could not get image'});
    }
    
}

export async function GET() {
    return NextResponse.json({ value: 'test' })
}
