import React, { useState } from 'react';

function UploadVideo() {
    const [file, setFile] = useState();
    const {shell} = window.require('electron');

    const changeHandler = (event) => {
        const fileValue = event.target.files[0]
        if (fileValue == null){
            return
        }

        const data = new FormData();
        data.append('file', fileValue)
        setFile(data);
    };

    const handleSubmission = () => {
        if (file == null) return
        fetch("/backend", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'path': file.get('file').path, 'fileName': file.get('file').name})
        }).then((response) => response.json())
            .then((data) => {
                console.log(data)
                if(data.status == '1') {
                    shell.showItemInFolder(data.filePath);
                }
            })
    };
    return (
        <>
            <div>
                <input type="file" name="file" onChange={changeHandler} accept=".mp4,.avi,.mov,.mkv,.wmv,.avchd" />
                <div>
                    <button onClick={handleSubmission}>Submit</button>
                </div>
            </div>
        </>
    )
}

export default UploadVideo