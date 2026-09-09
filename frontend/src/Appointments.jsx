import { useEffect, useState } from "react";
import { getAppointments, cancelAppointment } from "./api";

function Appointments({ patientName }) {
    const [appointments, setAppointments] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [cancellingId, setCancellingId] = useState(null);
    const [message, setMessage] = useState(null);

    const load = () => {
        if (!patientName.trim()) return;
        setLoading(true);
        setError(null);
        getAppointments(patientName.trim())
            .then((res) => setAppointments(res.data))
            .catch(() => setError("Couldn't load your appointments. Please try again."))
            .finally(() => setLoading(false));
    };

    useEffect(() => {
        load();
    }, [patientName]);

    const handleCancel = async (id) => {
        setCancellingId(id);
        setMessage(null);
        try {
            await cancelAppointment(id);
            setMessage({ type: "success", text: "Appointment cancelled." });
            load();
        } catch {
            setMessage({ type: "error", text: "Couldn't cancel. Please try again." });
        } finally {
            setCancellingId(null);
        }
    };

    if (!patientName.trim()) {
        return <div className="status">Enter your name above to see your appointments.</div>;
    }
    if (loading) return <div className="status">Loading your appointments...</div>;
    if (error) return <div className="status error">{error}</div>;

    const now = new Date();
    const upcoming = appointments.filter(
        (a) => a.status === "booked" && new Date(a.start_time) >= now
    );
    const past = appointments.filter(
        (a) => a.status === "cancelled" || new Date(a.start_time) < now
    );

    const renderCard = (a) => (
        <div key={a.id} className="slot-card">
            <div>
                <strong>{a.doctor_name}</strong>
            </div>
            <div>
                {new Date(a.start_time).toLocaleString()} –{" "}
                {new Date(a.end_time).toLocaleTimeString()}
            </div>
            <div className={`status-tag ${a.status}`}>{a.status}</div>
            {a.status === "booked" && new Date(a.start_time) >= now && (
                <button className="cancel-btn" onClick={() => handleCancel(a.id)} disabled={cancellingId === a.id}>
                    {cancellingId === a.id ? "Cancelling..." : "Cancel"}
                </button>
            )}
        </div>
    );

    return (
        <div>
            {message && <div className={`banner ${message.type}`}>{message.text}</div>}

            <h2>Upcoming</h2>
            {upcoming.length === 0 ? (
                <div className="status">No upcoming appointments.</div>
            ) : (
                <div className="slot-list">{upcoming.map(renderCard)}</div>
            )}

            <h2>Past / Cancelled</h2>
            {past.length === 0 ? (
                <div className="status">Nothing here yet.</div>
            ) : (
                <div className="slot-list">{past.map(renderCard)}</div>
            )}
        </div>
    );
}

export default Appointments;