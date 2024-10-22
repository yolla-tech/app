// BillItem type
export type BillItem = {
  name: string;
  price: number;
};

// Route type
export type Route = {
  walk_distance?: string; // In Python timedelta, in TS represented as ISO string or duration in string format
  public_transport_distance?: string;
  car_distance?: string;
};

// Bill type
export type Bill = {
  items?: BillItem[]; // Default is an empty array
  total_price?: number; // Default is 0.0
  expected_time?: string | null; // datetime can be represented as an ISO string
  to_route: Route;
  from_route: Route;
  from_address?: boolean; // Default is False
  to_address?: boolean; // Default is False
  link?: string | null; // Can be null or undefined
};
