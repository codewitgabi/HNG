import express from "express";
import { config } from "dotenv";
import logger from "morgan";
import axios from "axios";
config();

const app = express();
app.set("port", process.env.PORT || 3000);
const openweathermap_api_key = process.env.OPENWEATHERMAP_API_KEY;

// middlewares

app.use(logger("dev"));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// routes

app.get("/api/hello", async (req, res, next) => {
  try {
    const visitorName = req.query.visitor_name;

    var ip = req.headers["x-forwarded-for"] || req.socket.remoteAddress;

    console.log({ ip });

    await axios
      .get(`https://ipapi.co/json/`)
      .then(async (response) => {
        const data = response.data;

        await axios
          .get(
            `http://api.openweathermap.org/data/2.5/weather?appid=${openweathermap_api_key}&q=${data.city}`
          )
          .then((response) => {
            res.status(200).json({
              client_ip: data.ip,
              location: data.city,
              greeting: `Hello, ${visitorName}!, the temperature is ${Math.round(
                response.data.main.temp - 273
              )} degrees Celcius in ${data.city}`,
            });
          })
          .catch((error) => next(error));
      })
      .catch((error) => {
        next(error);
      });
  } catch (e) {
    next(e);
  }
});

app.use("*", (req, res) => {
  res.status(404).json({ message: "Not found" });
});

app.use((err, req, res, next) => {
  res.status(err.status || 500).json({ message: err.message });
});

app.listen(app.get("port"), "0.0.0.0", () => {
  console.log(`Server listening on ${app.get("port")}`);
});
