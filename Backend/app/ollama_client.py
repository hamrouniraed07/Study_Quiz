import requests
import json
import re

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434", model="llama3.2:3b"):
        self.base_url = base_url
        self.model = model
        print(f"🤖 Ollama Client initialisé avec le modèle: {model}")
    
    def generate(self, prompt, system_prompt=None, temperature=0.7):
        """
        Génère une réponse avec Ollama
        Optimisé pour GTX 1650 Ti
        """
        url = f"{self.base_url}/api/generate"
        
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "top_p": 0.9,
                "num_predict": 2000,
                "num_ctx": 2048,
                "num_gpu": 1,
                "num_thread": 6
            }
        }
        
        try:
            print(f"📤 Envoi de la requête à Ollama...")
            response = requests.post(url, json=payload, timeout=120)
            response.raise_for_status()
            result = response.json()
            generated_text = result.get("response", "")
            print(f"✅ Réponse reçue ({len(generated_text)} caractères)")
            return generated_text
        except requests.exceptions.ConnectionError:
            print("❌ Erreur: Ollama n'est pas démarré!")
            print("💡 Exécutez: ollama serve")
            return None
        except Exception as e:
            print(f"❌ Erreur Ollama: {e}")
            return None
    
    def clean_json_string(self, text):
        """
        Nettoie agressivement le texte pour obtenir un JSON valide
        """
        # Supprimer les markdown
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        text = text.strip()
        
        # Extraire uniquement le JSON array
        json_match = re.search(r'\[\s*\{.*\}\s*\]', text, re.DOTALL)
        if json_match:
            text = json_match.group(0)
        
        # Remplacer les échappements problématiques
        # Remplacer \" par "
        text = text.replace('\\"', '"')
        
        # Supprimer les backslashes isolés
        text = re.sub(r'\\(?!["\\/bfnrt])', '', text)
        
        # Remplacer les sauts de ligne dans les strings par des espaces
        # Pour éviter les problèmes de parsing
        lines = text.split('\n')
        cleaned_lines = []
        in_string = False
        
        for line in lines:
            # Compter les guillemets non échappés
            quote_count = len(re.findall(r'(?<!\\)"', line))
            
            if in_string:
                # On est dans une string, remplacer par un espace
                if cleaned_lines:
                    cleaned_lines[-1] += ' ' + line.strip()
            else:
                cleaned_lines.append(line)
            
            # Toggle in_string si nombre impair de guillemets
            if quote_count % 2 == 1:
                in_string = not in_string
        
        text = '\n'.join(cleaned_lines)
        
        return text
    
    def extract_json(self, text):
        """
        Extrait et nettoie le JSON d'une réponse
        """
        return self.clean_json_string(text)
    
    def is_alive(self):
        """Vérifie si Ollama est actif"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False