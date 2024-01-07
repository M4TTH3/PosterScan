"use client"
// tutorial i followed
// https://innocentanyaele.medium.com/create-a-drag-and-drop-file-component-in-reactjs-nextjs-tailwind-6ae70ba06e4b
import { useRef, useState } from "react";
export default async function Upload() {
    const [dragActive, setDragActive] = useState<boolean>(false);
    const inputRef = useRef<any>(null);
    const [files, setFiles] = useState<any>([]);

    function handleChange(e: any) {
        e.preventDefault();
        console.log("File has been added");
        if (e.target.files && e.target.files[0]) {
            for (let i = 0; i < e.target.files["length"]; i++) {
                setFiles((prevState: any) => [...prevState, e.target.files[i]]);
            }
        }
    }

    function handleSubmitFile(e: any) {
        e?.preventDefault();
        if (files.length === 0) {
            console.log("no file has been submitted");
            // no file has been submitted
        } else {
            console.log("Successfully submitted");
        }
    }

    function handleDrop(e: any) {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            for (let i = 0; i < e.dataTransfer.files["length"]; i++) {
                setFiles((prevState: any) => [...prevState, e.dataTransfer.files[i]]);
            }
        }
    }

    function handleDragLeave(e: any) {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
    }

    function handleDragOver(e: any) {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(true);
    }

    function handleDragEnter(e: any) {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(true);
    }

    function removeFile(fileName: any, idx: any) {
        const newArr = [...files];
        newArr.splice(idx, 1);
        setFiles([]);
        setFiles(newArr);
    }

    function openFileExplorer() {
        inputRef.current.value = "";
        inputRef.current.click();
    }

    return (
        <>
        <div className="text-black">hello hello?? hello can you see me</div>
            <div className="my-12 flex justify-center items-center">
                <div className="p-4 container w-auto h-auto bg-gray-100 border-1 rounded-lg">
                    <div className="flex justify-center mx-auto">
                        <div className=" border-2 py-2 px-4 bg-black text-white rounded-lg ">Please upload the image of the poster</div>
                    </div>
                    <div className="my-4 flex justify-center">
                        <form
                            className={`${dragActive ? "bg-blue-400" : "bg-blue-100"
                                }  p-4 w-[100%] rounded-lg  min-h-[10rem] text-center flex flex-col items-center justify-center`}
                            onDragEnter={handleDragEnter}
                            onSubmit={handleSubmitFile}
                            onDrop={handleDrop}
                            onDragLeave={handleDragLeave}
                            onDragOver={handleDragOver}
                        >

                            <input
                                placeholder="fileInput"
                                className="hidden"
                                ref={inputRef}
                                type="file"
                                multiple={true}
                                onChange={handleChange}
                                accept=".xlsx,.xls,image/*,.doc, .docx,.ppt, .pptx,.txt,.pdf"
                            />

                            <p>
                                Drag & Drop files or{" "}
                                <span
                                    className="font-bold text-blue-600 cursor-pointer"
                                    onClick={openFileExplorer}
                                >
                                    <u>Select files</u>
                                </span>{" "}
                                to upload
                            </p>

                            <div className="flex flex-col items-center p-3">
                                {files.map((file: any, idx: any) => (
                                    <div key={idx} className="flex flex-row space-x-5">
                                        <span>{file.name}</span>
                                        <span
                                            className="text-red-500 cursor-pointer"
                                            onClick={() => removeFile(file.name, idx)}
                                        >
                                            remove
                                        </span>
                                    </div>
                                ))}
                            </div>
                            <button type="submit" className="flex mx-auto bg-white hover:bg-gray-100 text-gray-800 font-semibold py-2 px-4 border border-gray-400 rounded shadow">
                                Submit Image
                            </button>

                        </form>


                    </div>
                </div>

            </div>


        </>


    )
}