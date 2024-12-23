// types.ts

// Represents the distance details for a route
export type Route = {
  walk_distance: string;
  public_transport_distance: string;
  car_distance: string;
};

// Represents an item with a name and price
export type Item = {
  name: string;
  price: number;
};

// Represents a cargo service with detailed information
export type CargoService = {
  id: string;
  service_name: string;
  items: Item[];
  total_price: number;
  expected_time: string | null;
  to_route: Route;
  from_route: Route;
  from_address: boolean; // Indicates if the from address is set
  to_address: boolean;   // Indicates if the to address is set
  link: string | null;
};

// Represents the properties of a box
export type BoxProperties = {
  width: number;
  height: number;
  length: number;
  weight: number;
};

// Base input type for search queries
export type BaseInput = {
  location_a: [number, number];
  location_b: [number, number];
  servis_type?: string;
  extra_services?: string[];
};

// Input type for box searches, extending BaseInput with box properties
export type BoxInput = BaseInput & {
  properties: BoxProperties;
};

// Input type for letter searches, extending BaseInput
export type LetterInput = BaseInput;

// Represents the weights used in search algorithms
export type SearchWeights = {
  price_weight: number;
  time_weight: number;
  walk_to_distance_weight: number;
  public_to_transport_distance_weight: number;
  car_to_distance_weight: number;
  walk_from_distance_weight: number;
  public_from_transport_distance_weight: number;
  car_from_distance_weight: number;
};

// Represents a geographical location with coordinates and a human-readable address
export type Location = {
  coords: [number, number]; // [latitude, longitude]
  address: string;
};

// Represents the state of selected "From" and "To" locations
export type SelectedLocations = {
  from: Location | null;
  to: Location | null;
};

// Represents the response from reverse geocoding API
export type ReverseGeocodeResponse = {
  display_name: string;
  address: {
    city?: string;
    town?: string;
    village?: string;
    hamlet?: string;
    [key: string]: any; // For any additional address components
  };
};

export type LocationOption = {
  label: string; // Display name
  value: Location; // Actual Location data
};