'use client'
import React, { useState } from 'react';

const Upload = () => {
  const [image, setImage] = useState('');
  const [apiResponse, setApiResponse] = useState(null);

  const handleImageChange = async (e: any) => {
    const file = e.target.files[0];
    const base64: any = await convertToBase64(file);
    setImage(base64);
  };

  const convertToBase64 = (file: any) => {
    return new Promise((resolve, reject) => {
      const fileReader = new FileReader();
      fileReader.readAsDataURL(file);
      fileReader.onload = () => resolve(fileReader.result);
      fileReader.onerror = (error) => reject(error);
    });
  };

  const handleSubmit = async () => {
    try {
        const apiCall = await fetch(
          '/api/ical', 
          {
            method: "POST",
            headers: {
              'content-type': 'application/json'
            },
            body: JSON.stringify({image: image})
          }
        )

        if (apiCall.status != 200) throw Error(apiCall.statusText);

        const fileBlob = await apiCall.blob();
        var link = document.createElement('a')  // once we have the file buffer BLOB from the post request we simply need to send a GET request to retrieve the file data
        link.href = window.URL.createObjectURL(fileBlob)
        link.download = 'posterscan.ics';
        link.click()
        link.remove();  //afterwards we remove the element 
      } 
      catch (error) {
        console.error('Error posting image to api/ical', error);
      }
  };

  return (
    <div className="flex flex-col items-center justify-center p-6 space-y-4">
      <div className='pl-[20%] md:pl-[5%]'>
        <input 
          type="file" 
          accept=".jpg,.png" 
          onChange={handleImageChange}
          className="file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100"
        />
      </div>
      <button 
        onClick={handleSubmit}
        className="text-center px-6 py-2 bg-blue-500 text-white font-bold rounded hover:bg-blue-700"
      >
        Upload
      </button>
      {image && <img src={image} alt="Uploaded" className="max-w-xs rounded-lg shadow-lg" />}
      {apiResponse && (
        <div className="text-center p-4 bg-gray-100 rounded-lg">
          <h3 className="text-lg font-semibold">API Response:</h3>
          <pre className="text-sm text-gray-600">{JSON.stringify(apiResponse, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default Upload;
