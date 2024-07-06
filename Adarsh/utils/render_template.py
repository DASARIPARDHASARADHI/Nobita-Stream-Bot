<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{heading}</title>
    <style>
        body {
            font-family: "Arial Black", sans-serif;
            background-color: #2c2c2c;
            color: #fff;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        h5 {
            color: #ddd;
            margin-bottom: 20px;
            text-align: center; /* Center text */
        }
        .button-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100%; /* Full width */
            max-width: 400px; /* Adjust as needed */
            padding: 0 20px; /* Added padding */
        }
        .button-container button {
            font-size: 16px; /* Adjusted font size */
            margin: 8px;
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            display: flex;
            align-items: center;
            transition: transform 0.2s, box-shadow 0.2s, opacity 0.2s;
            color: #fff;
            font-weight: bold;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            background-image: linear-gradient(
                45deg,
                rgba(255, 255, 255, 0.2) 50%,
                transparent 50%
            );
            background-size: 200% 200%;
            transition: background-position 0.5s;
            width: 100%; /* Full width */
        }
        .button-container button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.2);
            opacity: 0.9;
            background-position: 100%;
        }
        .button-container img {
            margin-right: 8px;
            width: 26px;
            height: 26px;
        }
        .mx-button {
            background-color: #0088cc;
        }
        .vlc-button {
            background-color: #ff8f00;
        }
        .playit-button {
            background-color: #d32f2f;
        }
        .save-button {
            background-color: #673ab7;
        }
        .telegram-button {
            background-color: #009688;
        }
        .playit-button + .save-button {
            margin-top: 24px;
        }

        @media screen and (max-width: 600px) {
            .button-container {
                max-width: 300px; /* Adjust for smaller screens */
            }
            .button-container button {
                font-size: 14px; /* Decrease font size further */
            }
        }
    </style>
</head>
<body>
    <h5>Click on the button below to watch/download in your favorite player</h5>
    <div class="button-container">
        <!-- Your buttons here -->
    </div>
</body>
</html>
