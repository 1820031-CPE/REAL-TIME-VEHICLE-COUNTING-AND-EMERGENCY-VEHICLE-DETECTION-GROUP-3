<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YOLO Vehicle Counting</title>
    <style>
        body {
            text-align: center;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            font-family: Arial, sans-serif;
        }
        h1 {
            color: #333;
            margin-top: 20px;
            font-size: 2.5em;
        }
        img {
            max-width: 90%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-top: 20px;
        }
        /* Additional styles */
        .container {
            width: 80%;
            margin: 30px auto;
        }
        .footer {
            margin-top: 40px;
            padding: 20px;
            background-color: #222;
            color: white;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>YOLO Vehicle Counting</h1>
        <img src="{{ url_for('video_feed') }}" alt="Object Detection">
    </div>
    <div class="footer">
        <p>© 2023 YOLO Object Detection. All rights reserved.</p>
    </div>
</body>
</html>
