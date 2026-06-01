import cv2
import uuid
import subprocess
import os

from detector import detect
from offside import determine_offside


def process_video(video_path):

    cap = cv2.VideoCapture(video_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 30

    unique_id = str(uuid.uuid4())

    raw_output = f"outputs/{unique_id}.avi"
    final_output = f"{unique_id}.mp4"

    writer = cv2.VideoWriter(
        raw_output,
        cv2.VideoWriter_fourcc(*'XVID'),
        fps,
        (width, height)
    )

    if not writer.isOpened():
        raise Exception("Failed to create output video")

    final_verdict = "UNKNOWN"

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        detections = detect(frame)

        attackers = []
        defenders = []

        for d in detections:

            x1, y1, x2, y2 = d["bbox"]
            label = d["label"]

            if label == "attacker":

                color = (0, 0, 255)

                attackers.append({
                    "x": x2
                })

            elif label == "defender":

                color = (255, 0, 0)

                defenders.append({
                    "x": x2
                })

            elif label == "referee":

                color = (0, 255, 255)

            elif label == "ball":

                color = (0, 255, 0)

            else:

                color = (255, 255, 255)

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                color,
                2
            )

            cv2.putText(
                frame,
                label.upper(),
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

        verdict = determine_offside(
            attackers,
            defenders
        )

        final_verdict = verdict

        cv2.putText(
            frame,
            f"VERDICT: {verdict}",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

        cv2.putText(
            frame,
            f"Attackers: {len(attackers)}",
            (30, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

        cv2.putText(
            frame,
            f"Defenders: {len(defenders)}",
            (30, 140),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 0),
            2
        )

        writer.write(frame)

    cap.release()
    writer.release()

    ffmpeg_output = f"outputs/{final_output}"

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            raw_output,
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            ffmpeg_output
        ],
        check=True
    )

    if os.path.exists(raw_output):
        os.remove(raw_output)

    return final_verdict, final_output

