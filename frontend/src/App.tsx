import React, { useState } from "react";
import axios, { AxiosError } from "axios";
import {
  CargoService,
  BoxProperties,
  SearchWeights,
  BoxInput,
  LetterInput,
} from "./types";
import { FaEnvelope, FaBox } from "react-icons/fa";
import "./App.css";
import { Toaster, toast } from "react-hot-toast";

const CargoServiceCard: React.FC<{ service: CargoService }> = ({ service }) => {
  const formatDuration = (duration: string): string => {
    const regex = /PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/;
    const matches = duration.match(regex);

    if (!matches) return "0s";

    const hours = matches[1] ? `${matches[1]}h ` : "";
    const minutes = matches[2] ? `${matches[2]}m ` : "";
    const seconds = matches[3] ? `${matches[3]}s` : "";

    return `${hours}${minutes}${seconds}`.trim();
  };

  return (
    <div className="cargo-service-card">
      <h3>{service.service_name}</h3>
      <ul>
        {service.items.map((item, index) => (
          <li key={index}>
            {item.name}: {item.price} TL
          </li>
        ))}
      </ul>
      <p>
        <strong>Total Price:</strong> {service.total_price} TL
      </p>
      <p>
        <strong>Expected Arrival Time:</strong>{" "}
        {service.expected_time ? service.expected_time : "N/A"}
      </p>
      <div className="route-info">
        <p>
          <strong>To Route:</strong>
        </p>
        <p>Walk Distance: {formatDuration(service.to_route.walk_distance)}</p>
        <p>
          Public Transport Distance:{" "}
          {formatDuration(service.to_route.public_transport_distance)}
        </p>
        <p>Car Distance: {formatDuration(service.to_route.car_distance)}</p>
      </div>
      <div className="route-info">
        <p>
          <strong>From Route:</strong>
        </p>
        <p>Walk Distance: {formatDuration(service.from_route.walk_distance)}</p>
        <p>
          Public Transport Distance:{" "}
          {formatDuration(service.from_route.public_transport_distance)}
        </p>
        <p>Car Distance: {formatDuration(service.from_route.car_distance)}</p>
      </div>
    </div>
  );
};

const App: React.FC = () => {
  const [locationA, setLocationA] = useState<string>("");
  const [locationB, setLocationB] = useState<string>("");
  const [cargoPrices, setCargoPrices] = useState<CargoService[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [mode, setMode] = useState<"letter" | "box">("letter");
  const [boxProperties, setBoxProperties] = useState<BoxProperties>({
    width: 1,
    height: 1,
    length: 1,
    weight: 1,
  });

  const getSearchWeights = () => {
    const searchWeights: SearchWeights = {
      price_weight: 1,
      time_weight: 0,
      walk_to_distance_weight: 0,
      public_to_transport_distance_weight: 0,
      car_to_distance_weight: 0,
      walk_from_distance_weight: 0,
      public_from_transport_distance_weight: 0,
      car_from_distance_weight: 0,
    };
    return searchWeights;
  };

  const handleBoxSearch = () => {
    const boxInput: BoxInput = {
      location_a: locationA,
      location_b: locationB,
      servis_type: "default",
      extra_services: [],
      properties: boxProperties,
    };

    return axios.post("http://127.0.0.1:8000/search_box", {
      box: boxInput,
      weights: getSearchWeights(),
    });
  };

  const handleLetterSearch = () => {
    const letterInput: LetterInput = {
      location_a: locationA,
      location_b: locationB,
      servis_type: "default",
      extra_services: [],
    };

    return axios.post("http://127.0.0.1:8000/search_letter", {
      letter: letterInput,
      weights: getSearchWeights(),
    });
  };

  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await (mode === "box"
        ? handleBoxSearch()
        : handleLetterSearch());
      toast.success("Cargo prices fetched successfully!");
      setCargoPrices(response.data);
    } catch (error) {
      console.error("Error fetching cargo prices:", error);
      if (error instanceof AxiosError) {
        const axiosError: AxiosError = error;
        const responseData = axiosError.response?.data as any;
        toast.error(
          `Error fetching cargo prices. 
          Status: ${axiosError.status} \n 
          Status Text: ${axiosError.response?.statusText}
          Detail Text: ${responseData?.detail}
          `
        );
      }
    }
    setLoading(false);
  };

  return (
    <div className="app">
      <Toaster />
      <h1>Cargo Service Price Listing</h1>
      <div className="mode-selector">
        <button
          className={`mode-button ${mode === "letter" ? "active" : ""}`}
          onClick={() => setMode("letter")}
        >
          <FaEnvelope size={24} /> Letter
        </button>
        <button
          className={`mode-button ${mode === "box" ? "active" : ""}`}
          onClick={() => setMode("box")}
        >
          <FaBox size={24} /> Box
        </button>
      </div>
      <div className="form">
        <label>
          From Location (Location A):
          <input
            type="text"
            value={locationA}
            onChange={(e) => setLocationA(e.target.value)}
          />
        </label>
        <label>
          To Location (Location B):
          <input
            type="text"
            value={locationB}
            onChange={(e) => setLocationB(e.target.value)}
          />
        </label>
        {mode === "box" && (
          <div className="box-properties">
            <label>
              Width (cm):
              <input
                type="number"
                value={boxProperties.width}
                onChange={(e) =>
                  setBoxProperties({
                    ...boxProperties,
                    width: parseFloat(e.target.value),
                  })
                }
              />
            </label>
            <label>
              Height (cm):
              <input
                type="number"
                value={boxProperties.height}
                onChange={(e) =>
                  setBoxProperties({
                    ...boxProperties,
                    height: parseFloat(e.target.value),
                  })
                }
              />
            </label>
            <label>
              Length (cm):
              <input
                type="number"
                value={boxProperties.length}
                onChange={(e) =>
                  setBoxProperties({
                    ...boxProperties,
                    length: parseFloat(e.target.value),
                  })
                }
              />
            </label>
            <label>
              Weight (kg):
              <input
                type="number"
                value={boxProperties.weight}
                onChange={(e) =>
                  setBoxProperties({
                    ...boxProperties,
                    weight: parseFloat(e.target.value),
                  })
                }
              />
            </label>
          </div>
        )}
        <button
          className="search-button"
          onClick={handleSearch}
          disabled={loading}
        >
          {loading ? "Searching..." : "Search Cargo Services"}
        </button>
      </div>

      {cargoPrices.length > 0 && (
        <div className="cargo-prices">
          <h2>Available Cargo Services</h2>
          {cargoPrices.map((service, index) => (
            <CargoServiceCard key={index} service={service} />
          ))}
        </div>
      )}
    </div>
  );
};

export default App;
