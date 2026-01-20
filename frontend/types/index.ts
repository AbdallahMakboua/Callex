// types/index.ts
export interface Doctor {
  id: string;
  name: string;
  specialty: string;
  hospital: string;
  timeSlot: string;
  experience: string;
  rating: number;
}

export interface Message {
  id: string;
  role: 'user' | 'ai';
  content: string;
  type: 'text' | 'doctor-list';
  data?: Doctor[]; // Optional: Only present if type is 'doctor-list'
}