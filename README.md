# Black-Jack

♠️ Blackjack (Java + Python)
Un'implementazione completa del gioco Blackjack basata su architettura Client-Server. Il progetto utilizza Java per il motore di gioco (backend logico) e Python (Tkinter) per l'interfaccia grafica (frontend), comunicando tramite TCP Sockets.

(Sostituisci questo link con una tua immagine dopo aver caricato il progetto)

🚀 Caratteristiche
Architettura Distribuita: Logica e Grafica sono completamente separate e comunicano via rete locale (localhost).

Sistema di Scommesse: Gestione del saldo utente, puntate variabili (10€, 50€, 100€) e controlli anti-bancarotta.

Regole Complete: Include Hit, Stand e la complessa meccanica dello Split (divisione della mano in caso di carte uguali).

Dealer AI: Il banco gioca automaticamente seguendo la regola "Soft 17" (pesca fino a 17).

Multithreading: Il client Python utilizza thread separati per ascoltare il server senza bloccare l'interfaccia grafica.

Protocollo Custom: Protocollo testuale personalizzato per lo scambio dati (es. BET:10, CARTA:k_cuori, SPLIT).

🛠️ Tecnologie Utilizzate
Backend (Server)
Linguaggio: Java

Concetti: Socket Programming (java.net), Input/Output Streams, OOP (Classi Mano, Mazzo, Carta), Gestione stati di gioco.

Frontend (Client)
Linguaggio: Python 3

Librerie: tkinter (GUI), socket (Rete), threading (Asincronia), PIL / Pillow (Gestione Immagini).
