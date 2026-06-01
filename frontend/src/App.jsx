import { useState } from "react";
import axios from "axios";

function App() {

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [verdict, setVerdict] = useState("");
  const [videoUrl, setVideoUrl] = useState("");

  const handleUpload = async () => {

    if (!file) {
      alert("Please select a video.");
      return;
    }

    try {

      setLoading(true);

      const formData = new FormData();
      formData.append("video", file);

      /* const response = await axios.post(
        "http://localhost:8000/process",
        formData
      ); */

      /* For Deployment*/
      const response = await axios.post(
        "/process",
        formData
      );
      /* For Deployment*/
      
      console.log(response.data);

      setVerdict(response.data.verdict);
      setVideoUrl(response.data.video_url);

    } catch (error) {

      console.error(error);

      alert(
        error.response?.data?.detail ||
        error.message
      );

    } finally {

      setLoading(false);

    }
  };

  return (
    <div
      style={{
        padding: "30px",
        fontFamily: "Arial"
      }}
    >
      <h1>Football Offside Detection</h1>

      <input
        type="file"
        accept="video/*"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br /><br />

      <button onClick={handleUpload}>
        Analyze Video
      </button>

      {loading && (
        <p>Processing video...</p>
      )}

      {verdict && (
        <h2>
          Verdict: {verdict}
        </h2>
      )}

      {videoUrl && (
        <div>
          <h3>Processed Video</h3>

          <video
            width="900"
            controls
            preload="metadata"
          >
            <source
              src={videoUrl}
              type="video/mp4"
            />

            Your browser does not support HTML5 video.
          </video>
        </div>
      )}
    </div>
  );
}

export default App;



