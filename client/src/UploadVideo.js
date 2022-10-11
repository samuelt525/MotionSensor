import React, { useState } from 'react';

function UploadVideo() {
    const [file, setFile] = useState();

    const changeHandler = (event) => {
        setFile(event.target.files[0]);
    };

    const handleSubmission = () => {
        //cannot jsonstringify file object

        const body = {
            'lastModified': file.lastModified,
            'lastModifiedDate': file.lastModifiedDate,
            'name': file.name,
            'size': file.size,
            'type': file.type
        }
        fetch("/backend", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        }).then((response) => response.json())
            .then((data) => console.log(data))
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