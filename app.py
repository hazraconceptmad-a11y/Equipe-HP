import React, { useState, useEffect, useMemo } from 'react';
import { 
  LayoutDashboard, 
  Package, 
  ShoppingCart, 
  BarChart3, 
  MessageSquare, 
  Phone, 
  Search, 
  Plus, 
  Trash2, 
  Edit3, 
  CheckCircle2, 
  XCircle, 
  ArrowLeft, 
  Download, 
  Mic, 
  Camera, 
  Send,
  Calculator,
  Info
} from 'lucide-react';

// --- CONFIGURATION ---
const ACCESS_CODE = "hp+2626";
const EXPIRY_DATE = new Date('2026-12-31');
const MEMBERS = ["Tantely", "Eliane", "Perline", "Mbolasahy", "Elia", "Mamy"];
const CATEGORIES = ["Parapharmacie", "Médicaments", "Tests"];

const App = () => {
  // --- STATE ---
  const [currentPage, setCurrentPage] = useState('access');
  const [accessInput, setAccessInput] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState('');
  const [currentTime, setCurrentTime] = useState(new Date());
  
  // Data State
  const [stocks, setStocks] = useState([]);
  const [preVente, setPreVente] = useState([]);
  const [ventesDefinitives, setVentesDefinitives] = useState([]);
  const [messages, setMessages] = useState([]);
  const [contacts, setContacts] = useState(MEMBERS.reduce((acc, name) => ({ ...acc, [name]: "" }), {}));

  // Calendar State
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [activeCategory, setActiveCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  // IA State
  const [iaInfo, setIaInfo] = useState(null);

  // --- CLOCK ---
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // --- AUTH LOGIC ---
  const handleLogin = () => {
    if (accessInput === ACCESS_CODE && currentUser) {
      if (new Date() > EXPIRY_DATE) {
        alert("Efa lany daty ny fahazoan-dalana hampiasa ity site ity (31 Dec 2026).");
        return;
      }
      setIsAuthenticated(true);
      setCurrentPage('articles');
    } else {
      alert("Code diso na tsy nifidy anarana ianao.");
    }
  };

  // --- HELPER FUNCTIONS ---
  const formatDate = (dateStr) => {
    const d = new Date(dateStr);
    return d.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' });
  };

  const getFilteredStocks = () => {
    let filtered = stocks;
    if (activeCategory !== 'all') {
      filtered = filtered.filter(item => item.category === activeCategory);
    }
    if (searchQuery) {
      filtered = filtered.filter(item => item.name.toLowerCase().includes(searchQuery.toLowerCase()));
    }
    return filtered.sort((a, b) => a.name.localeCompare(b.name));
  };

  const handleAddToPreVente = (item, qty) => {
    const newItem = {
      id: Date.now(),
      articleId: item.id,
      name: item.name,
      price: item.priceVente,
      priceAchat: item.priceAchat,
      qty: parseInt(qty),
      total: item.priceVente * qty,
      date: selectedDate
    };
    setPreVente([...preVente, newItem]);
  };

  const validateVentes = () => {
    const newVentes = preVente.map(item => ({ ...item, timestamp: new Date().getTime() }));
    setVentesDefinitives([...ventesDefinitives, ...newVentes]);
    
    // Update Stocks
    const updatedStocks = stocks.map(s => {
      const sold = preVente.filter(p => p.articleId === s.id).reduce((acc, curr) => acc + curr.qty, 0);
      return { ...s, count: s.count - sold };
    });
    setStocks(updatedStocks);
    setPreVente([]);
    alert("Voamarina ny varotra!");
  };

  // --- IA AGENT LOGIC ---
  const askIA = (article) => {
    const info = {
      name: article.name,
      dosage: "1 isaky ny 8 ora (rehefa avy nisakafo)",
      target: "Olon-dehibe sy ankizy mihoatra ny 12 taona",
      posologie: "3 pilina isan'andro mandritra ny 5 andro",
      contraindication: "Tsy azo ampiasaina raha misy allergy amin'ny " + article.name,
      sideEffects: "Mety mampanidina loha na mampanaintaina kibo kely"
    };
    setIaInfo(info);
  };

  // --- PDF EXPORT MOCK ---
  const downloadPDF = (withPrice) => {
    const list = getFilteredStocks();
    let content = "HAZRAPHARMA - LISTE DES ARTICLES\n\n";
    list.forEach(item => {
      content += `- ${item.name} ${withPrice ? `(${item.priceVente} Ar)` : ''}\n`;
    });
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `liste_articles_${withPrice ? 'prix' : 'simple'}.txt`;
    link.click();
  };

  // --- COMPONENTS ---

  const Header = () => (
    <div className="bg-emerald-700 text-white p-4 shadow-lg flex justify-between items-center">
      <div>
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <span className="bg-white text-emerald-700 px-2 py-0.5 rounded-lg">HP+</span> HAZRAPHARMA
        </h1>
        <p className="text-xs opacity-80">VENTE 2026 | Mpampiasa: {currentUser}</p>
      </div>
      <div className="text-right">
        <p className="text-sm font-mono">{currentTime.toLocaleDateString()} - {currentTime.toLocaleTimeString()}</p>
        <p className="text-[10px] text-emerald-200">Daty voafidy: {formatDate(selectedDate)}</p>
      </div>
    </div>
  );

  const Navigation = () => (
    <div className="flex overflow-x-auto bg-white border-b sticky top-0 z-10 no-scrollbar">
      {[
        { id: 'articles', label: 'Articles', icon: Package },
        { id: 'stocks', label: 'Stocks', icon: LayoutDashboard },
        { id: 'vente', label: 'Vente', icon: ShoppingCart },
        { id: 'analyse', label: 'Analyse', icon: BarChart3 },
        { id: 'communication', label: 'Chat', icon: MessageSquare },
        { id: 'contacts', label: 'Contacts', icon: Phone },
      ].map((tab) => (
        <button
          key={tab.id}
          onClick={() => setCurrentPage(tab.id)}
          className={`flex flex-col items-center p-3 min-w-[80px] text-xs transition-colors ${
            currentPage === tab.id ? 'text-emerald-600 border-b-2 border-emerald-600' : 'text-gray-500'
          }`}
        >
          <tab.icon size={20} className="mb-1" />
          {tab.label}
        </button>
      ))}
    </div>
  );

  // --- VIEWS ---

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-slate-100 flex flex-col items-center justify-center p-6 font-sans">
        <div className="bg-white p-8 rounded-2xl shadow-2xl w-full max-w-md text-center border-t-8 border-emerald-600">
          <div className="text-6xl mb-4 text-emerald-600 font-black italic">HP+</div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">HAZRAPHARMA</h1>
          <h2 className="text-lg text-emerald-600 font-semibold mb-6">VENTE 2026</h2>
          
          <div className="space-y-4 text-left">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Anaran'ny Mpikambana</label>
              <select 
                className="w-full p-3 border rounded-xl bg-gray-50 focus:ring-2 focus:ring-emerald-500 outline-none"
                value={currentUser}
                onChange={(e) => setCurrentUser(e.target.value)}
              >
                <option value="">-- Mifidiana anarana --</option>
                {MEMBERS.map(m => <option key={m} value={m}>{m}</option>)}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Code fidirana (hp+...)</label>
              <input 
                type="password" 
                placeholder="Ampidiro ny code..."
                className="w-full p-3 border rounded-xl bg-gray-50 focus:ring-2 focus:ring-emerald-500 outline-none"
                value={accessInput}
                onChange={(e) => setAccessInput(e.target.value)}
              />
            </div>

            <div className="pt-4">
              <p className="text-[10px] text-gray-400 mb-2">Androany: {currentTime.toLocaleString()}</p>
              <button 
                onClick={handleLogin}
                className="w-full bg-emerald-600 text-white py-4 rounded-xl font-bold hover:bg-emerald-700 transition shadow-lg"
              >
                HIDITRA NY SITE
              </button>
            </div>
          </div>
          <p className="mt-8 text-[10px] text-gray-400">Valable jusqu'au 31 Décembre 2026</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col max-w-lg mx-auto border-x shadow-2xl overflow-hidden relative">
      <Header />
      <Navigation />

      <main className="flex-1 overflow-y-auto pb-20 p-4">
        {/* PAGE ARTICLES */}
        {currentPage === 'articles' && (
          <div className="space-y-4">
            <div className="flex gap-2">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-3 text-gray-400" size={18} />
                <input 
                  type="text" 
                  placeholder="Hikaroka article..." 
                  className="w-full pl-10 p-2.5 bg-white border rounded-xl text-sm"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
              <input 
                type="date" 
                className="p-2 border rounded-xl text-xs bg-white"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
              />
            </div>

            <div className="flex gap-2 overflow-x-auto pb-2 no-scrollbar">
              <button onClick={() => setActiveCategory('all')} className={`px-4 py-2 rounded-full text-xs whitespace-nowrap ${activeCategory === 'all' ? 'bg-emerald-600 text-white' : 'bg-white text-gray-600'}`}>Tsy an-kanavaka</button>
              {CATEGORIES.map(cat => (
                <button key={cat} onClick={() => setActiveCategory(cat)} className={`px-4 py-2 rounded-full text-xs whitespace-nowrap ${activeCategory === cat ? 'bg-emerald-600 text-white' : 'bg-white text-gray-600'}`}>{cat}</button>
              ))}
            </div>

            <div className="space-y-3">
              {getFilteredStocks().map(item => (
                <div key={item.id} className="bg-white p-4 rounded-2xl shadow-sm border border-gray-100">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <h3 className="font-bold text-gray-800">{item.name}</h3>
                      <p className="text-[10px] text-gray-400 uppercase">{item.category}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-emerald-600 font-bold">{item.priceVente} Ar</p>
                      <p className={`text-[10px] font-semibold ${new Date(item.expiry) < new Date(new Date().setMonth(new Date().getMonth() + 2)) ? 'text-red-500' : 'text-gray-400'}`}>
                        Lany: {formatDate(item.expiry)}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center justify-between mt-4 gap-4">
                    <div className="flex items-center gap-2">
                      <button onClick={() => askIA(item)} className="p-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition">
                        <Info size={18} />
                      </button>
                      <span className="text-[10px] text-gray-500 font-medium">Stock: {item.count}</span>
                    </div>
                    
                    <div className="flex items-center gap-2 bg-gray-50 p-1 rounded-xl">
                      <input 
                        id={`qty-${item.id}`}
                        type="number" 
                        defaultValue="1" 
                        min="1" 
                        max={item.count}
                        className="w-12 bg-transparent text-center font-bold text-sm outline-none"
                      />
                      <button 
                        onClick={() => {
                          const val = document.getElementById(`qty-${item.id}`).value;
                          handleAddToPreVente(item, val);
                        }}
                        className="bg-emerald-600 text-white px-4 py-1.5 rounded-lg text-xs font-bold"
                      >
                        OK
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="grid grid-cols-2 gap-2 pt-4">
              <button onClick={() => downloadPDF(true)} className="flex items-center justify-center gap-2 bg-slate-800 text-white p-3 rounded-xl text-xs">
                <Download size={16} /> PDF + Prix
              </button>
              <button onClick={() => downloadPDF(false)} className="flex items-center justify-center gap-2 bg-slate-100 text-slate-800 p-3 rounded-xl text-xs border">
                <Download size={16} /> PDF Liste
              </button>
            </div>
          </div>
        )}

        {/* PAGE STOCKS */}
        {currentPage === 'stocks' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="font-bold text-gray-700">FITANTANANA TAHIRY</h2>
              <button 
                onClick={() => {
                  const name = prompt("Anaran'ny article:");
                  const count = parseInt(prompt("Isany:"));
                  const priceAchat = parseInt(prompt("Prix d'Achat:"));
                  const priceVente = parseInt(prompt("Prix de Vente:"));
                  const category = prompt("Category (Médicaments, Parapharmacie, Tests):");
                  const expiry = prompt("Date Péremption (YYYY-MM-DD):");
                  if (name && count && priceAchat && priceVente && category) {
                    setStocks([...stocks, { 
                      id: Date.now(), 
                      name, 
                      count, 
                      priceAchat, 
                      priceVente, 
                      category, 
                      expiry,
                      location: "Rayon A"
                    }]);
                  }
                }}
                className="bg-emerald-600 text-white p-2 rounded-full shadow-lg"
              >
                <Plus size={20} />
              </button>
            </div>

            <div className="bg-white rounded-2xl p-4 shadow-sm border overflow-x-auto">
              <table className="w-full text-xs text-left">
                <thead>
                  <tr className="border-b text-gray-400 font-medium">
                    <th className="pb-2 pr-2">Art.</th>
                    <th className="pb-2 px-2">Qty</th>
                    <th className="pb-2 px-2">Achat</th>
                    <th className="pb-2 px-2">Vente</th>
                    <th className="pb-2 text-right">Marge</th>
                  </tr>
                </thead>
                <tbody>
                  {getFilteredStocks().map(item => (
                    <tr key={item.id} className="border-b last:border-0">
                      <td className="py-3 pr-2 font-medium">{item.name}</td>
                      <td className="py-3 px-2">{item.count}</td>
                      <td className="py-3 px-2 text-gray-400">{item.priceAchat}</td>
                      <td className="py-3 px-2 text-emerald-600 font-bold">{item.priceVente}</td>
                      <td className="py-3 text-right font-bold text-blue-600">+{item.priceVente - item.priceAchat}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="p-4 bg-emerald-50 rounded-2xl border border-emerald-100">
              <h4 className="text-xs font-bold text-emerald-800 mb-2 uppercase">Résumé Stock Final</h4>
              <div className="flex justify-between items-center">
                <span className="text-sm text-emerald-700">Total Articles:</span>
                <span className="text-lg font-black text-emerald-800">{stocks.reduce((a, b) => a + b.count, 0)}</span>
              </div>
            </div>
          </div>
        )}

        {/* PAGE VENTE */}
        {currentPage === 'vente' && (
          <div className="space-y-6">
             <div className="bg-white p-4 rounded-2xl shadow-sm border">
               <h3 className="text-sm font-bold text-gray-700 mb-4 flex items-center gap-2">
                 <ShoppingCart size={18} className="text-emerald-600" /> PRÉ-VENTE
               </h3>
               {preVente.length === 0 ? (
                 <p className="text-xs text-center text-gray-400 py-4 italic">Tsy misy komanda eo am-piandrasana</p>
               ) : (
                 <div className="space-y-3">
                   {preVente.map(item => (
                     <div key={item.id} className="flex justify-between items-center border-b pb-2">
                       <div>
                         <p className="text-xs font-bold">{item.name}</p>
                         <p className="text-[10px] text-gray-400">{item.qty} x {item.price} Ar</p>
                       </div>
                       <div className="flex items-center gap-3">
                         <span className="text-xs font-bold text-emerald-600">{item.total} Ar</span>
                         <button onClick={() => setPreVente(preVente.filter(p => p.id !== item.id))} className="text-red-400"><Trash2 size={14}/></button>
                       </div>
                     </div>
                   ))}
                   <div className="pt-2 border-t flex justify-between items-center">
                     <span className="text-sm font-bold">TOTAL:</span>
                     <span className="text-lg font-black text-emerald-600">{preVente.reduce((a, b) => a + b.total, 0)} Ar</span>
                   </div>
                   <button onClick={validateVentes} className="w-full bg-emerald-600 text-white py-3 rounded-xl text-sm font-bold mt-2 shadow-md">
                     VALIDER LE LISTE (Vente Définitive)
                   </button>
                 </div>
               )}
             </div>

             <div className="space-y-4">
                <h3 className="text-sm font-bold text-gray-700">VENTE DÉFINITIVE PAR JOUR</h3>
                <div className="bg-white p-2 rounded-2xl shadow-sm border overflow-x-auto">
                  <table className="w-full text-[10px]">
                    <thead>
                      <tr className="bg-gray-50 text-gray-400">
                        <th className="p-2">Anarana</th>
                        <th className="p-2">Qty</th>
                        <th className="p-2">Vente</th>
                        <th className="p-2">Tombony</th>
                      </tr>
                    </thead>
                    <tbody>
                      {ventesDefinitives.filter(v => v.date === selectedDate).map(v => (
                        <tr key={v.id} className="border-b">
                          <td className="p-2 font-medium">{v.name}</td>
                          <td className="p-2 text-center">{v.qty}</td>
                          <td className="p-2 text-emerald-600">{v.total}</td>
                          <td className="p-2 text-blue-600">{(v.price - v.priceAchat) * v.qty}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
             </div>
          </div>
        )}

        {/* PAGE ANALYSE */}
        {currentPage === 'analyse' && (
          <div className="space-y-4">
            <h2 className="font-bold text-gray-700">ANALYSE DE VENTE</h2>
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-white p-4 rounded-2xl border-l-4 border-emerald-500 shadow-sm">
                <p className="text-[10px] text-gray-400 uppercase font-bold">Total Niditra</p>
                <p className="text-lg font-black text-gray-800">
                  {ventesDefinitives.filter(v => v.date === selectedDate).reduce((a, b) => a + b.total, 0)} Ar
                </p>
              </div>
              <div className="bg-white p-4 rounded-2xl border-l-4 border-blue-500 shadow-sm">
                <p className="text-[10px] text-gray-400 uppercase font-bold">Tombony Madio</p>
                <p className="text-lg font-black text-gray-800">
                  {ventesDefinitives.filter(v => v.date === selectedDate).reduce((a, b) => a + (b.price - b.priceAchat) * b.qty, 0)} Ar
                </p>
              </div>
            </div>
            
            <div className="bg-slate-800 text-white p-6 rounded-3xl space-y-4">
               <h3 className="text-sm font-bold border-b border-slate-700 pb-2">Vola Isan-kerin'andro (Mock)</h3>
               <div className="flex justify-between items-center">
                 <span className="text-xs text-slate-400 italic">Alatsinainy - Sabotsy</span>
                 <span className="text-xl font-bold text-emerald-400">--- Ar</span>
               </div>
            </div>
          </div>
        )}

        {/* PAGE COMMUNICATION */}
        {currentPage === 'communication' && (
          <div className="space-y-4">
             <div className="bg-white rounded-2xl shadow-sm border h-[400px] flex flex-col">
                <div className="p-3 border-b flex gap-2">
                  {['Urgence', 'Filazana', 'SMS'].map(cat => (
                    <button key={cat} className="flex-1 text-[10px] py-2 rounded-lg bg-gray-50 border font-bold hover:bg-emerald-50 hover:text-emerald-700 transition">
                      {cat}
                    </button>
                  ))}
                </div>
                <div className="flex-1 p-4 overflow-y-auto space-y-3 bg-slate-50">
                  {messages.map(m => (
                    <div key={m.id} className={`max-w-[80%] p-3 rounded-2xl text-xs ${m.user === currentUser ? 'bg-emerald-600 text-white ml-auto' : 'bg-white border text-gray-700'}`}>
                      <p className="font-black text-[9px] mb-1 opacity-70 uppercase">{m.user}</p>
                      <p>{m.text}</p>
                      <p className="text-[8px] text-right mt-1 opacity-50">{m.time}</p>
                    </div>
                  ))}
                </div>
                <div className="p-3 border-t bg-white flex items-center gap-2">
                   <button className="p-2 text-gray-400 hover:text-emerald-600 transition"><Camera size={18}/></button>
                   <button className="p-2 text-gray-400 hover:text-emerald-600 transition"><Mic size={18}/></button>
                   <input 
                    type="text" 
                    id="chat-input"
                    placeholder="Hanatra hafatra..." 
                    className="flex-1 bg-gray-50 border rounded-full px-4 py-2 text-xs outline-none"
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') {
                        const val = e.target.value;
                        if (val) {
                          setMessages([...messages, { id: Date.now(), user: currentUser, text: val, time: new Date().toLocaleTimeString() }]);
                          e.target.value = '';
                        }
                      }
                    }}
                   />
                   <button 
                    onClick={() => {
                      const input = document.getElementById('chat-input');
                      if (input.value) {
                        setMessages([...messages, { id: Date.now(), user: currentUser, text: input.value, time: new Date().toLocaleTimeString() }]);
                        input.value = '';
                      }
                    }}
                    className="bg-emerald-600 text-white p-2 rounded-full"
                   >
                     <Send size={16}/>
                   </button>
                </div>
             </div>
          </div>
        )}

        {/* PAGE CONTACTS */}
        {currentPage === 'contacts' && (
          <div className="space-y-4">
             <h2 className="font-bold text-gray-700 mb-4">NUMÉRO TÉLÉPHONE</h2>
             {MEMBERS.map(m => (
               <div key={m} className="bg-white p-4 rounded-2xl shadow-sm border flex items-center gap-4">
                 <div className="w-10 h-10 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-700 font-bold">
                    {m[0]}
                 </div>
                 <div className="flex-1">
                   <p className="text-sm font-bold text-gray-700">{m}</p>
                   <input 
                    type="tel" 
                    placeholder="03x xx xxx xx"
                    value={contacts[m]}
                    onChange={(e) => setContacts({...contacts, [m]: e.target.value})}
                    className="w-full text-xs text-gray-400 bg-transparent border-none outline-none focus:text-emerald-600 font-mono"
                   />
                 </div>
                 <Edit3 size={16} className="text-gray-300" />
               </div>
             ))}
          </div>
        )}
      </main>

      {/* IA OVERLAY */}
      {iaInfo && (
        <div className="absolute inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-end p-4">
          <div className="bg-white w-full rounded-3xl p-6 shadow-2xl animate-in slide-in-from-bottom duration-300">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-black text-blue-600 flex items-center gap-2">
                <Info size={20} /> IA PHARMACIEN : {iaInfo.name}
              </h3>
              <button onClick={() => setIaInfo(null)}><XCircle className="text-gray-300" /></button>
            </div>
            
            <div className="space-y-4 text-xs">
              <div className="bg-blue-50 p-3 rounded-xl">
                <p className="font-bold text-blue-800 mb-1">Dosage & Posologie:</p>
                <p className="text-blue-700">{iaInfo.dosage} - {iaInfo.posologie}</p>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-gray-50 p-3 rounded-xl">
                  <p className="font-bold text-gray-700 mb-1">Ho an'iza:</p>
                  <p className="text-gray-600">{iaInfo.target}</p>
                </div>
                <div className="bg-red-50 p-3 rounded-xl">
                  <p className="font-bold text-red-800 mb-1">Tsy mahazo mampiasa:</p>
                  <p className="text-red-700">{iaInfo.contraindication}</p>
                </div>
              </div>
              <div className="bg-orange-50 p-3 rounded-xl">
                <p className="font-bold text-orange-800 mb-1">Effets indésirables:</p>
                <p className="text-orange-700">{iaInfo.sideEffects}</p>
              </div>
              <button onClick={() => setIaInfo(null)} className="w-full bg-blue-600 text-white py-3 rounded-xl font-bold mt-2">NAZAVINA</button>
            </div>
          </div>
        </div>
      )}

      {/* FOOTER NAVBAR (Fixed on Mobile) */}
      <div className="fixed bottom-0 w-full max-w-lg bg-white border-t flex justify-around p-2 text-[10px] text-gray-400 shadow-[0_-2px_10px_rgba(0,0,0,0.05)]">
        <div className="text-center font-bold text-emerald-600">
          <p>HAZRAPHARMA</p>
          <p>2026</p>
        </div>
        <div className="text-center">
          <p>DATE: {formatDate(selectedDate)}</p>
          <p>{currentTime.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</p>
        </div>
        <div className="text-center">
          <p>USER: {currentUser || '---'}</p>
          <p className="text-emerald-500 font-bold uppercase">Online</p>
        </div>
      </div>
    </div>
  );
};

export default App;
