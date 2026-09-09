import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export const getSlots = () => axios.get(`${API_BASE}/slots`);

export const bookSlot = (slotId, patientName) =>
    axios.post(`${API_BASE}/appointments`, { slot_id: slotId, patient_name: patientName });

export const getAppointments = (patientName) =>
    axios.get(`${API_BASE}/appointments`, { params: { patient_name: patientName } });

export const cancelAppointment = (appointmentId) =>
    axios.patch(`${API_BASE}/appointments/${appointmentId}/cancel`);