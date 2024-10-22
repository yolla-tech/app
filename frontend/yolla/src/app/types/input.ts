// BaseInput type
export type BaseInput = {
  location_a: string;
  location_b: string;
  servis_type?: string; // Default value handled in backend
  extra_services?: string[]; // Default is an empty array
};

// LetterInput type (inherits from BaseInput)
export type LetterInput = BaseInput;

// BoxProperties type
export type BoxProperties = {
  width?: number; // Default value handled in backend
  height?: number; // Default value handled in backend
  length?: number; // Default value handled in backend
  weight?: number; // Default value handled in backend
};

// BoxInput type (inherits from BaseInput and adds properties)
export type BoxInput = BaseInput & {
  properties: BoxProperties;
};
