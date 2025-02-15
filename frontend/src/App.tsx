import React, { useState, useRef, useEffect } from "react";
import AsyncSelect from "react-select/async";
import axios, { AxiosError } from "axios";
import { FaEnvelope, FaBox, FaUserCircle } from "react-icons/fa";
import {
  CargoService,
  BoxProperties,
  SearchWeights,
  BoxInput,
  LetterInput,
  SelectedLocations,
  ReverseGeocodeResponse
} from "./types";

import { Toaster, toast } from "react-hot-toast";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMapEvents,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import customRedMarker from "./assets/marker-icon-red.png";
import markerShadow from "./assets/marker-shadow.png";
import "./App.css";

delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

const customRedIcon = new L.Icon({
  iconUrl: customRedMarker,
  shadowUrl: markerShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

const fetchCitySuggestions = async (inputValue: string) => {
  if (!inputValue) return [];

  const response = await fetch(
    `https://nominatim.openstreetmap.org/search?` +
    new URLSearchParams({
      q: inputValue,
      format: "json",
      addressdetails: "1",
      limit: "5",
    })
  );
  const data = await response.json();

  return data.map((item: any) => ({
    label: item.display_name,
    value: item.display_name,
    lat: item.lat,
    lon: item.lon,
  }));
};

function useOnScreen(ref: React.RefObject<HTMLDivElement>, rootMargin = "0px") {
  const [isIntersecting, setIntersecting] = useState(false);

  useEffect(() => {
    if (!ref.current) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIntersecting(true);
          observer.unobserve(entry.target);
        }
      },
      { rootMargin }
    );
    observer.observe(ref.current);
    return () => {
      observer.disconnect();
    };
  }, [ref, rootMargin]);

  return isIntersecting;
}

const FadeInSection: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const ref = useRef<HTMLDivElement>(null);
  const isVisible = useOnScreen(ref, "-100px");

  return (
    <div
      ref={ref}
      className={`fade-in-section ${isVisible ? "visible" : ""}`}
    >
      {children}
    </div>
  );
};

const MapClickHandler: React.FC<{
  setSelectedLocations: React.Dispatch<React.SetStateAction<SelectedLocations>>;
  selectedLocations: SelectedLocations;
}> = ({ setSelectedLocations, selectedLocations }) => {
  useMapEvents({
    click: async (e) => {
      const { lat, lng } = e.latlng;
      const coords: [number, number] = [lat, lng];

      try {
        //CONVERTING COORDINATES INTO READIBLE NAMES
        const response = await axios.get<ReverseGeocodeResponse>(
          "https://nominatim.openstreetmap.org/reverse",
          {
            params: {
              format: "jsonv2",
              lat,
              lon: lng,
            },
          }
        );

        const address =
          response.data.address.city ||
          response.data.address.town ||
          response.data.address.village ||
          response.data.address.hamlet ||
          "Unknown Location";

        if (!selectedLocations.from) {
          setSelectedLocations({
            ...selectedLocations,
            from: { coords, address },
          });
          toast.success(`Nereden: ${address}`);
        } else if (!selectedLocations.to) {
          setSelectedLocations({
            ...selectedLocations,
            to: { coords, address },
          });
          toast.success(`Nereye: ${address}`);
        } else {
          setSelectedLocations({
            from: { coords, address },
            to: null,
          });
          toast(`Nereden sıfırlandı: ${address}`, {
            icon: "ℹ️",
            style: {
              background: "#e0f7fa",
              color: "#006064",
            },
          });
        }
      } catch (error) {
        console.error("Error in reverse geocoding:", error);
        toast.error("Failed to retrieve address from coordinates.");
      }
    },
  });

  return null;
};

//CARGO SERVICE
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
        <strong>Toplam Fiyat:</strong> {service.total_price} TL
      </p>
      <p>
        <strong>Tahmini Varış Süresi:</strong> {service.expected_time ?? "N/A"}
      </p>

      <div className="route-info">
        <p><strong>Nereye (En Yakın Şube)</strong></p>
        <p>Yürüyerek: {formatDuration(service.to_route.walk_distance)}</p>
        <p>
          Toplu Taşıma:{" "}
          {formatDuration(service.to_route.public_transport_distance)}
        </p>
        <p>Araba: {formatDuration(service.to_route.car_distance)}</p>
      </div>

      <div className="route-info">
        <p><strong>Nereden (En Yakın Şube)</strong></p>
        <p>Yürüyerek: {formatDuration(service.from_route.walk_distance)}</p>
        <p>
          Toplu Taşıma:{" "}
          {formatDuration(service.from_route.public_transport_distance)}
        </p>
        <p>Araba: {formatDuration(service.from_route.car_distance)}</p>
      </div>
    </div>
  );
};
// MAIN APP
const App: React.FC = () => {
  const [cargoPrices, setCargoPrices] = useState<CargoService[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const [mode, setMode] = useState<"letter" | "box">("letter");
  const [boxProperties, setBoxProperties] = useState<BoxProperties>({
    width: 1,
    height: 1,
    length: 1,
    weight: 1,
  });

  const [selectedLocations, setSelectedLocations] = useState<SelectedLocations>({
    from: null,
    to: null,
  });

  // Weights for search
  const getSearchWeights = () => ({
    price_weight: 1,
    time_weight: 0,
    walk_to_distance_weight: 0,
    public_to_transport_distance_weight: 0,
    car_to_distance_weight: 0,
    walk_from_distance_weight: 0,
    public_from_transport_distance_weight: 0,
    car_from_distance_weight: 0,
  });

  // Box search
  const handleBoxSearch = () => {
    const boxInput: BoxInput = {
      location_a: (selectedLocations.from?.coords) || [39.92077, 32.85411],
      location_b: (selectedLocations.to?.coords) || [39.92077, 32.85411],
      servis_type: "default",
      extra_services: [],
      properties: boxProperties,
    };
    return axios.post(
      "https://key-anemone-full.ngrok-free.app/api/search_box",
      {
        box: boxInput,
        weights: getSearchWeights(),
      }
    );
  };

  // Letter search
  const handleLetterSearch = () => {
    const letterInput: LetterInput = {
      location_a: selectedLocations.from?.coords || [39.92077, 32.85411],
      location_b: selectedLocations.to?.coords || [39.92077, 32.85411],
      servis_type: "default",
      extra_services: [],
    };
    return axios.post(
      "https://key-anemone-full.ngrok-free.app/api/search_letter",
      {
        letter: letterInput,
        weights: getSearchWeights(),
      }
    );
  };

  // Main search handler
  const handleSearch = async () => {
    if (!selectedLocations.from || !selectedLocations.to) {
      toast.error("Lütfen haritadan Nereden ve Nereye seçiniz.");
      return;
    }
    setLoading(true);
    try {
      const response =
        mode === "box" ? await handleBoxSearch() : await handleLetterSearch();
      setCargoPrices(response.data);
      toast.success("Kargo fiyatları getirildi!");
    } catch (error) {
      console.error("Error fetching cargo prices:", error);
      if (error instanceof AxiosError) {
        const axiosError: AxiosError = error;
        const responseData = axiosError.response?.data as any;
        toast.error(
          `Kargo fiyatları alınırken hata oluştu. 
          Status: ${axiosError.status} 
          Status Text: ${axiosError.response?.statusText}
          Detail Text: ${responseData?.detail}`
        );
      }
    }
    setLoading(false);
  };

  const defaultPosition: [number, number] = selectedLocations.from
    ? selectedLocations.from.coords
    : [39.92077, 32.85411];

  return (
    <div className="app">
      <Toaster />

      <nav className="navbar">
        <div className="logo">yolla</div>
        <div className="user-icon">
          <FaUserCircle size={24} />
        </div>
      </nav>

      <div className="content-container">
        <div className="left-panel">
          <h1>
            Selam <span role="img" aria-label="wave">👋</span> Nereye yollayalım?
          </h1>
          <div className="mode-selector">
            <button
              className={`mode-button ${mode === "letter" ? "active" : ""}`}
              onClick={() => setMode("letter")}
            >
              <FaEnvelope /> Zarf
            </button>
            <button
              className={`mode-button ${mode === "box" ? "active" : ""}`}
              onClick={() => setMode("box")}
            >
              <FaBox /> Kutu
            </button>
          </div>

          <div className="form">
            <label>
              Nereden?
              <AsyncSelect
                cacheOptions
                loadOptions={fetchCitySuggestions}
                placeholder="Bir konum secin"
                defaultOptions
                value={
                  selectedLocations.from
                    ? {
                      label: selectedLocations.from.address,
                      value: selectedLocations.from.address,
                      lat: selectedLocations.from.coords[0],
                      lon: selectedLocations.from.coords[1],
                    }
                    : null
                }
                onChange={(selected: any) => {
                  if (!selected) return;
                  const { value, lat, lon } = selected;

                  setSelectedLocations((prev) => ({
                    ...prev,
                    from: {
                      coords: [parseFloat(lat), parseFloat(lon)],
                      address: value,
                    },
                  }));

                  toast.success(`Nereden: ${value}`);
                }}
              />
            </label>

            <label>
              Nereye?
              <AsyncSelect
                cacheOptions
                loadOptions={fetchCitySuggestions}
                placeholder="Bir konum secin"
                defaultOptions
                value={
                  selectedLocations.to
                    ? {
                      label: selectedLocations.to.address,
                      value: selectedLocations.to.address,
                      lat: selectedLocations.to.coords[0],
                      lon: selectedLocations.to.coords[1],
                    }
                    : null
                }
                onChange={(selected: any) => {
                  if (!selected) return;
                  const { value, lat, lon } = selected;

                  setSelectedLocations((prev) => ({
                    ...prev,
                    to: {
                      coords: [parseFloat(lat), parseFloat(lon)],
                      address: value,
                    },
                  }));

                  toast.success(`Nereye: ${value}`);
                }}
              />
            </label>

            {mode === "box" && (
              <div className="box-properties">
                <label>
                  Ağırlık (kg):
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
                <label>
                  En/Boy/Yükseklik (cm):
                  <div className="dimensions-row">
                    <input
                      type="number"
                      placeholder="En"
                      value={boxProperties.width}
                      onChange={(e) =>
                        setBoxProperties({
                          ...boxProperties,
                          width: parseFloat(e.target.value),
                        })
                      }
                    />
                    <input
                      type="number"
                      placeholder="Boy"
                      value={boxProperties.length}
                      onChange={(e) =>
                        setBoxProperties({
                          ...boxProperties,
                          length: parseFloat(e.target.value),
                        })
                      }
                    />
                    <input
                      type="number"
                      placeholder="Yükseklik"
                      value={boxProperties.height}
                      onChange={(e) =>
                        setBoxProperties({
                          ...boxProperties,
                          height: parseFloat(e.target.value),
                        })
                      }
                    />
                  </div>
                </label>
              </div>
            )}
          </div>

          <button
            className="search-button"
            onClick={handleSearch}
            disabled={loading}
          >
            {loading ? "Aranıyor..." : "ARA"}
          </button>

          {cargoPrices.length > 0 && (
            <div className="cargo-prices">
              <h2>Mevcut Kargo Servisleri</h2>
              {cargoPrices.map((service, idx) => (
                <CargoServiceCard key={idx} service={service} />
              ))}
            </div>
          )}
        </div>

        <div className="right-panel">
          <MapContainer
            center={defaultPosition}
            zoom={selectedLocations.from || selectedLocations.to ? 13 : 5}
            scrollWheelZoom={true}
            style={{ height: "100%", width: "100%" }}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">
                OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <MapClickHandler
              setSelectedLocations={setSelectedLocations}
              selectedLocations={selectedLocations}
            />
            {selectedLocations.from && (
              <Marker
                position={selectedLocations.from.coords}
                icon={customRedIcon}
              >
                <Popup>Nereden: {selectedLocations.from.address}</Popup>
              </Marker>
            )}
            {selectedLocations.to && (
              <Marker
                position={selectedLocations.to.coords}
                icon={customRedIcon}
              >
                <Popup>Nereye: {selectedLocations.to.address}</Popup>
              </Marker>
            )}
          </MapContainer>
        </div>
      </div>

      <section className="biz-kimiz-section">
        <h2>Biz Kimiz?</h2>
        <div className="cards-container">
          <FadeInSection>
            <div className="info-card">Durak Durak Takip Et</div>
          </FadeInSection>
          <FadeInSection>
            <div className="info-card">Adresi Değiştir</div>
          </FadeInSection>
          <FadeInSection>
            <div className="info-card">Zamanı Değiştir</div>
          </FadeInSection>
          <FadeInSection>
            <div className="info-card">Kolay İade Et</div>
          </FadeInSection>
        </div>
      </section>
    </div>
  );
};

export default App;
