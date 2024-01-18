import type { NextApiRequest, NextApiResponse } from 'next';
import { NextResponse } from 'next/server';
import axios from 'axios';

export async function POST(req: NextApiRequest) {

    console.log('running')

    if (req.method != 'POST') {
        return NextResponse.json({ message: 'Only POST requests allowed' }, { status: 500 });
    }

    try {
        const chunks = [];
        for await (const chunk of req.body) {
            chunks.push(chunk);
        }

        const bodyString = Buffer.concat(chunks).toString('utf-8');
        const image_obj = JSON.parse(bodyString);
        image_obj['image'] = image_obj['image'].split(',')[1]; // Remove the base64 description

        const scanPosterResponse = await axios.post('http://localhost:5000/api/scanposter', image_obj);
        const iCalSettings = scanPosterResponse.data;

        const iCalResponse = await axios.post('http://localhost:5000/api/getical', iCalSettings);
        const icalContents = iCalResponse.data;

        console.log(icalContents)

        //  res.headers["Content-Disposition"] = "attachment; filename=calendar.ics"

        return new NextResponse(icalContents, {
            status: 200, 
            headers: {
                'content-type': 'text/calendar',
                "content-disposition": "attachment; filename=calendar.ics"
            }
        });
    } catch (error) {
        console.error('Error processing image', error);
        return NextResponse.json({ message: 'Could not get image' }, { status: 500 });
    }
}
