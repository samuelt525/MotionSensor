import React, {useState} from 'react';

function UploadVideo() {
    const [file, setFile] = useState();
    const [isFileSet, setIsFileSet] = useState(false);

    const changeHandler = (event) => {
        setFile(event.target.files[0]);
        setIsFileSet(true);
    };

    const handleSubmission = () => {
        console.log('wee');
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