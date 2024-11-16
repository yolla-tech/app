export type Route = {
  walk_distance: string;
  public_transport_distance: string;
  car_distance: string;
};

export type Item = {
  name: string;
  price: number;
};

export type CargoService = {
  id: string;
  service_name: string;
  items: Item[];
  total_price: number;
  expected_time: string | null;
  to_route: Route;
  from_route: Route;
  from_address: boolean;
  to_address: boolean;
  link: string | null;
};

export type BoxProperties = {
  width: number;
  height: number;
  length: number;
  weight: number;
};

export type BaseInput = {
  location_a: string;
  location_b: string;
  servis_type?: string;
  extra_services?: string[];
};

export type BoxInput = BaseInput & {
  properties: BoxProperties;
};

export type LetterInput = BaseInput;

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
