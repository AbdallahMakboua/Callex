import { Doctor } from '@/types';
// CHANGE: Replaced UserMd with Stethoscope
import { Clock, MapPin, Star, Stethoscope } from 'lucide-react'; 

interface Props {
  doctor: Doctor;
  onBook: (doc: Doctor) => void;
}

export default function DoctorCard({ doctor, onBook }: Props) {
  return (
    <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm min-w-[260px] flex flex-col justify-between">
      <div>
        <div className="flex items-start justify-between mb-2">
          <div className="flex items-center gap-2">
            <div className="p-2 bg-blue-50 rounded-full text-blue-600">
              {/* CHANGE: Use Stethoscope here */}
              <Stethoscope size={20} />
            </div>
            <div>
              <h3 className="font-bold text-gray-900 text-sm">{doctor.name}</h3>
              <p className="text-xs text-blue-600 font-medium">{doctor.specialty}</p>
            </div>
          </div>
          <div className="flex items-center text-amber-500 text-xs font-bold">
            <Star size={12} fill="currentColor" className="mr-1" />
            {doctor.rating}
          </div>
        </div>
        
        <div className="space-y-1.5 text-xs text-gray-500 mb-4">
          <div className="flex items-center gap-1.5">
            <MapPin size={12} /> {doctor.hospital}
          </div>
          <div className="flex items-center gap-1.5">
            <Clock size={12} /> {doctor.timeSlot}
          </div>
        </div>
      </div>

      <button 
        onClick={() => onBook(doctor)}
        className="w-full py-2 bg-gray-900 text-white text-xs font-medium rounded-lg hover:bg-black transition-colors"
      >
        Book Now
      </button>
    </div>
  );
}