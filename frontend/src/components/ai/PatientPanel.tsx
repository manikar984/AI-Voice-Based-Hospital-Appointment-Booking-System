interface ConversationMemory {
    intent?: string;
    doctor?: string;
    date?: string;
    time?: string;
    phone?: string;
    patient_name?: string;
}

interface PatientPanelProps {
    memory: ConversationMemory;
}

function PatientPanel({ memory }: PatientPanelProps) {
    return (
        <div className="rounded-xl border bg-white p-5 shadow-md w-80">

            <h2 className="text-lg font-bold mb-4">
                Active Patient
            </h2>

            <div className="space-y-3">

                <div>
                    <strong>Name:</strong> {memory.patient_name || "--"}
                </div>

                <div>
                    <strong>Phone:</strong> {memory.phone || "--"}
                </div>

                <div>
                    <strong>Intent:</strong> {memory.intent || "--"}
                </div>

                <div>
                    <strong>Doctor:</strong> {memory.doctor || "--"}
                </div>

                <div>
                    <strong>Date:</strong> {memory.date || "--"}
                </div>

                <div>
                    <strong>Time:</strong> {memory.time || "--"}
                </div>

            </div>

        </div>
    );
}

export default PatientPanel;