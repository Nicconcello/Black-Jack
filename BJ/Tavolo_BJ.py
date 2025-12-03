import tkinter as tk
from PIL import Image, ImageTk
import socket
import threading
import random

carta_coperta_label = None

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9999))

risposta = client.recv(1024).decode()
print(risposta)

def carica_carta(percorso_file, larghezza, altezza):
    """
    Funzione che carica un'immagine, la ridimensiona e
    restituisce l'oggetto pronto per Tkinter.
    """
    img_originale = Image.open(percorso_file)
    # 2. Ridimensiona l'immagine (metodo LANCZOS per alta qualità)
    img_ridimensionata = img_originale.resize((larghezza, altezza), Image.Resampling.LANCZOS)
    
    # 3. Converte per Tkinter
    foto_finale = ImageTk.PhotoImage(img_ridimensionata)
    return foto_finale

#Creare la finestra principale
root = tk.Tk()
root.title("Black Jack")
root.geometry("1000x1000")

# 2. Creare un Frame
# bg="darkgreen" serve per vederlo chiaramente, bd=5 è il bordo
mio_frame = tk.Frame(root, bg="darkgreen", bd=5, relief="sunken")

# 3. Posizionare il Frame nella finestra
mio_frame.pack(fill="both", expand=True, padx=20, pady=20)

frame_banco = tk.Frame(mio_frame, bg="darkgreen", bd=2, relief="ridge")

# Posizione: pack(side=TOP)
# fill="x" serve a estendere il frame per tutta la larghezza della finestra
frame_banco.pack(side=tk.TOP, fill="x", pady=10, padx=10)
# A. Una Label (Testo) che dice "BANCO"
# Nota: il genitore qui è 'frame_banco', non root!

scritta_banco = tk.Frame(frame_banco, bg="lightgrey", bd=2, relief="groove")
scritta_banco.pack(side=tk.TOP, fill="x", pady=10, padx=10)
label_banco = tk.Label(scritta_banco, text="BANCO", font=("Arial", 14, "bold"), bg="lightgray") # Stesso colore del frame per estetica
label_banco.pack(pady=5) # Un po' di margine verticale

carte_banco = tk.Frame(frame_banco, bg="darkgreen", bd=2, relief="groove", height=150)
carte_banco.pack(side=tk.BOTTOM, pady=10)



frame_info = tk.Frame(mio_frame, bg="darkgreen")
frame_info.pack(side=tk.TOP, fill="both", expand=True)
label_info = tk.Label(frame_info, text="", font=("Arial", 20), bg="darkgreen", fg="yellow")
label_info.pack(expand=True)

frame_player = tk.Frame(mio_frame, bg="darkgreen")
frame_player.pack(side=tk.BOTTOM, fill="x", pady=20)
area_carte = tk.Frame(frame_player, bg="darkgreen")
area_carte.pack(side=tk.TOP, pady=10)

# Mano Sinistra
carte_playerS = tk.Frame(area_carte, bg="darkgreen", bd=2, height=150, width=200)
carte_playerS.pack(side=tk.LEFT, padx=30) # padx=30 le distanzia tra loro

# Mano Destra (Principale)
carte_playerD = tk.Frame(area_carte, bg="darkgreen", bd=2, height=150, width=200)
carte_playerD.pack(side=tk.RIGHT, padx=30)

# --- SOTTO-CONTENITORE PER I PULSANTI ---
bottoni = tk.Frame(frame_player, bg="darkgreen")
bottoni.pack(side=tk.BOTTOM, pady=10, fill="x")

# 1. PANNELLO SCOMMESSE (Visibile all'inizio)
frame_scommesse = tk.Frame(bottoni, bg="darkgreen")
# Lo impacchettiamo subito perché è la prima cosa che si deve vedere
frame_scommesse.pack() 

# I bottoni delle fiches
btn_10 = tk.Button(frame_scommesse, text="10€", width=8, font=("Arial", 12, "bold"), bg="gold", command=lambda: manda_bet(10))
btn_10.pack(side=tk.LEFT, padx=5)

btn_50 = tk.Button(frame_scommesse, text="50€", width=8, font=("Arial", 12, "bold"), bg="gold", command=lambda: manda_bet(50))
btn_50.pack(side=tk.LEFT, padx=5)

btn_100 = tk.Button(frame_scommesse, text="100€", width=8, font=("Arial", 12, "bold"), bg="gold", command=lambda: manda_bet(100))
btn_100.pack(side=tk.LEFT, padx=5)

# Il tasto per confermare e iniziare
btn_deal = tk.Button(frame_scommesse, text="DAI CARTE", width=15, font=("Arial", 12, "bold"), bg="orange")
btn_deal.pack(side=tk.LEFT, padx=20)


# 2. PANNELLO GIOCO (Nascosto all'inizio)
frame_comandi = tk.Frame(bottoni, bg="darkgreen")
# NON facciamo .pack() qui! Lo faremo apparire solo dopo il DEAL.

# I bottoni di gioco (li mettiamo dentro frame_comandi invece che 'bottoni')
btn_carta = tk.Button(frame_comandi, text="CARTA", width=10, font=("Arial", 12))
btn_carta.pack(side=tk.LEFT, padx=5)

btn_stai = tk.Button(frame_comandi, text="STO", width=10, font=("Arial", 12))
btn_stai.pack(side=tk.LEFT, padx=5)

btn_rigioca = tk.Button(frame_comandi, text="RIGIOCA", width=10, font=("Arial", 12))
btn_rigioca.pack(side=tk.LEFT, padx=5)
btn_rigioca.config(state="disabled")

btn_split = tk.Button(frame_comandi, text="SPLIT", width=10, font=("Arial", 12))
btn_split.pack(side=tk.LEFT, padx=5)
btn_split.config(state="disabled")

# Il tasto ESCI magari lo vuoi sempre. Creiamo un frame piccolino in fondo per lui
frame_esci = tk.Frame(root, bg="darkgreen")
frame_esci.pack(side=tk.BOTTOM, pady=5)
btn_quit = tk.Button(frame_esci, text="ESCI", width=10, font=("Arial", 10))
btn_quit.pack()

def ascolta_server():
    global carta_coperta_label
    
    # Funzione interna per disegnare in sicurezza
    def disegna_carta_sicura(frame_destinazione, percorso_img, salva_in_variabile_globale=False):
        try:
            img = carica_carta(percorso_img, 100, 150)
            lbl = tk.Label(frame_destinazione, image=img, bg="forestgreen")
            lbl.pack(side=tk.LEFT, padx=5)
            lbl.image = img # Mantiene il riferimento
            
            if salva_in_variabile_globale:
                global carta_coperta_label
                carta_coperta_label = lbl
        except Exception as e:
            print(f"Errore grafico: {e}")

    # Funzione interna per distruggere carta coperta
    def rimuovi_carta_coperta():
        global carta_coperta_label
        if carta_coperta_label is not None:
            carta_coperta_label.destroy()
            carta_coperta_label = None

    while True:
        try:
            # Controllo vita finestra
            try:
                if not root.winfo_exists(): break
            except: break

            dati = client.recv(4096).decode()
            if not dati: break
            
            for msg in dati.split("\n"):
                msg = msg.strip()
                if not msg: continue
                
                print(f"MSG: {msg}") # Debug
                
                # --- GESTIONE CARTA GIOCATORE ---
                if "CARTA:" in msg or "CARTA_DX:" in msg or "CARTA_SX:" in msg:
                    # Passa alla grafica di gioco (in sicurezza)
                    root.after(0, mostra_fase_gioco)
                    
                    frame_dest = carte_playerD # Default
                    nome = ""
                    
                    if "CARTA_DX:" in msg:
                        nome = msg.replace("CARTA_DX:", "")
                        frame_dest = carte_playerD
                    elif "CARTA_SX:" in msg:
                        nome = msg.replace("CARTA_SX:", "")
                        frame_dest = carte_playerS
                    else:
                        nome = msg.replace("CARTA:", "")
                        frame_dest = carte_playerD
                    
                    path = r"PNG/" + nome + ".png"
                    # Ordina a Tkinter di disegnare (nel thread principale!)
                    root.after(0, lambda f=frame_dest, p=path: disegna_carta_sicura(f, p))

                # --- GESTIONE BANCO ---
                elif "BANCO:" in msg:
                    if "retro" in msg:
                        colore = random.choice(["nero", "rosso"])
                        path = r"PNG/retro_" + colore + ".png"
                        # Disegna e salva come carta coperta
                        root.after(0, lambda f=carte_banco, p=path: disegna_carta_sicura(f, p, True))
                    else:
                        # Rimuovi la vecchia carta coperta
                        root.after(0, rimuovi_carta_coperta)
                        
                        nome = msg.replace("BANCO:", "")
                        path = r"PNG/" + nome + ".png"
                        # Disegna la carta svelata/nuova
                        root.after(0, lambda f=carte_banco, p=path: disegna_carta_sicura(f, p))

                # --- ALTRI COMANDI ---
                elif "SALDO:" in msg:
                    parti = msg.replace("SALDO:", "").split(":")
                    soldi, puntata = parti[0], parti[1]
                    root.after(0, lambda: root.title(f"BLACKJACK - Saldo: {soldi}€ | Puntata: {puntata}€"))
                
                elif "MSG:" in msg:
                    txt = msg.replace("MSG:", "")
                    root.after(0, lambda: label_info.config(text=txt, fg="yellow"))
                    keywords = ["VINTO", "VINCE", "PERSO", "PERDE", "PAREGGIO", "PARI", "SBALLATO", "SBALLA"]
                    
                    # TRUCCO: Convertiamo il messaggio in maiuscolo (.upper()) prima di controllare
                    if any(parola in txt.upper() for parola in keywords):
                        root.after(0, lambda: btn_carta.config(state="disabled"))
                        root.after(0, lambda: btn_stai.config(state="disabled"))
                        root.after(0, lambda: btn_split.config(state="disabled"))
                        root.after(0, lambda: btn_rigioca.config(state="normal"))
                        
                elif "split" in msg.lower():
                    root.after(0, lambda: btn_split.config(state="normal"))

        except Exception as e:
            print("Errore ascolto:", e)
            break

        except Exception as e:
            print("Errore ricezione:", e)
            break

def chiudi_gioco():
    try:
        client.send("ESCI\n".encode())
    except Exception as e:
        print("ERRORE NELL'INVIO", e)
    root.destroy()
    
# Collega la funzione al click del mouse
btn_quit.config(command=chiudi_gioco)


def sto():
    try:
        client.send("STO\n".encode())
    except Exception as e1:
        print("ERRORE NELL'INVIO", e1)
        
btn_stai.config(command=sto)


def carta():
    try:
        client.send("CARTA\n".encode())
    except Exception as e2:
        print("ERRORE NELL'INVIO", e2)
        
btn_carta.config(command=carta)

def pulisci_tavolo():
    try:
        # Pulisce le carte
        for widget in carte_playerD.winfo_children(): widget.destroy()
        for widget in carte_playerS.winfo_children(): widget.destroy()     
        for widget in carte_banco.winfo_children(): widget.destroy()
        
        global carta_coperta_label
        carta_coperta_label = None
        
        label_info.config(text="Nuova partita...", fg="white")
        
        # CAMBIO SCENA (Senza parentesi!)
        root.after(0, mostra_fase_scommessa)
        
        # Reset Pulsanti
        btn_carta.config(state="normal")
        btn_stai.config(state="normal")
        btn_split.config(state="disabled")
        btn_rigioca.config(state="disabled")
        
    except Exception as e:
        print(f"Errore durante pulizia tavolo: {e}")

def rigioca():
    try:
        pulisci_tavolo()
        
        client.send("RESET\n".encode())
    except Exception as e3:
        print("ERRORE NELL'INVIO", e3)
        
btn_rigioca.config(command=rigioca)

def split():
    try:
        # --- CORREZIONE FONDAMENTALE ---
        # Spegniamo subito il bottone per impedire di premerlo una seconda volta
        btn_split.config(state="disabled") 
        # -------------------------------

        # 1. PULIZIA LOCALE (Il codice che avevi già)
        for widget in carte_playerD.winfo_children(): 
            widget.destroy()
        for widget in carte_playerS.winfo_children(): 
            widget.destroy()
            
        client.send("SPLIT\n".encode())
    except Exception as e4:
        print("ERRORE NELL'INVIO", e4)
        
btn_split.config(command=split)

def mostra_fase_scommessa():
    # Nascondi i comandi di gioco
    frame_comandi.pack_forget() 
    # Mostra le scommesse
    frame_scommesse.pack()
    # Aggiorna testo
    label_info.config(text="Fai la tua puntata...", fg="white")

def mostra_fase_gioco():
    # Nascondi le scommesse
    frame_scommesse.pack_forget()
    # Mostra i comandi di gioco
    frame_comandi.pack()
    # Aggiorna testo
    label_info.config(text="Partita in corso", fg="yellow")
    
def manda_bet(valore):
    try:
        messaggio = f"BET:{valore}\n" # <--- IL \n È FONDAMENTALE!
        print(f"PYTHON PROVA A INVIARE: '{messaggio.strip()}'")
        client.send(messaggio.encode())
        print("PYTHON: Invio completato.")
    except Exception as e:
        print(f"PYTHON ERRORE INVIO: {e}")

def manda_deal():
    try:
        print("PYTHON PROVA A INVIARE: 'DEAL'")
        client.send("DEAL\n".encode()) # <--- ANCHE QUI IL \n
    except Exception as e:
        print(f"PYTHON ERRORE DEAL: {e}")
        
btn_deal.config(command=manda_deal)
# ... tutto il tuo codice grafico ...

# AVVIO DEL THREAD DI ASCOLTO
t = threading.Thread(target=ascolta_server)
t.daemon = True 
t.start()

# --- PRIMA IL LIFT (ALZARE LA FINESTRA) ---
root.lift()
root.attributes('-topmost',True)
root.after_idle(root.attributes,'-topmost',False)

# Intercetta la chiusura della finestra
root.protocol("WM_DELETE_WINDOW", chiudi_gioco)
# --- POI IL MAINLOOP (FINE DEL CODICE) ---
root.after(100, mostra_fase_scommessa)

# %%
root.mainloop()
