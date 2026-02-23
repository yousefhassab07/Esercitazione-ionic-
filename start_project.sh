#!/bin/bash
echo "--- AVVIO SUSHI PROJECT ---"

# Avvia MySQL (per sicurezza)
sudo service mysql start

# Avvia il Backend in background
echo "1. Avvio Backend Flask..."
python3 backend/app.py > backend.log 2>&1 &
BACKEND_PID=$!

# Aspetta qualche secondo che il backend parta
sleep 5

# Avvia il Pannello Staff in background
echo "2. Avvio Pannello Staff (Angular)..."
cd frontend/sushi-staff
# Usiamo --host 0.0.0.0 per renderlo accessibile dal browser in Codespace
npx ng serve --host 0.0.0.0 --disable-host-check --port 4200 > ../../staff.log 2>&1 &
STAFF_PID=$!
cd ../..

# Avvia l'App Cliente in background
echo "3. Avvio App Cliente (Ionic)..."
cd frontend/sushi-client
npx ionic serve --external --no-open --port 8100 > ../../client.log 2>&1 &
CLIENT_PID=$!
cd ../..

echo "--- TUTTO AVVIATO! ---"
echo "Controlla la scheda 'PORTS' (Porte) in basso o di lato in VS Code."
echo "Troverai tre link cliccabili:"
echo " - Porta 4200: Pannello Staff"
echo " - Porta 8100: App Cliente"
echo " - Porta 5000: Backend API"
echo ""
echo "Per fermare tutto, premi CTRL+C e chiudi il terminale."
echo "I log sono salvati in backend.log, staff.log e client.log"

# Mantieni lo script attivo per non chiudere i processi
wait $BACKEND_PID $STAFF_PID $CLIENT_PID
