import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchDistricts, fetchConstituencies } from '../api/client';

export default function Home() {
  const navigate = useNavigate();
  const [districts, setDistricts] = useState([]);
  const [constituencies, setConstituencies] = useState([]);
  const [selectedDistrict, setSelectedDistrict] = useState('');
  const [selectedConstituency, setSelectedConstituency] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDistricts()
      .then(setDistricts)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (selectedDistrict) {
      setSelectedConstituency('');
      fetchConstituencies(selectedDistrict)
        .then(setConstituencies)
        .catch(console.error);
    } else {
      setConstituencies([]);
    }
  }, [selectedDistrict]);

  const handleExplore = () => {
    const params = new URLSearchParams();
    if (selectedDistrict) params.set('district', selectedDistrict);
    if (selectedConstituency) params.set('constituency', selectedConstituency);
    navigate(`/candidates?${params.toString()}`);
  };

  return (
    <div className="min-h-[calc(100vh-3.5rem)]">
      {/* Hero Section */}
      <section className="relative bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
          <div className="max-w-3xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent-50 text-accent-700 text-xs font-medium mb-6">
              <span className="w-1.5 h-1.5 rounded-full bg-accent-500"></span>
              Kerala Assembly Elections
            </div>
            <h1 className="text-3xl sm:text-5xl font-bold text-neutral-900 tracking-tight mb-4">
              Know Your <span className="text-accent-600">Candidate</span>
            </h1>
            <p className="text-neutral-500 text-base sm:text-lg max-w-xl mx-auto mb-10 leading-relaxed">
              Explore candidate backgrounds, compare profiles side by side, and rank them based on what matters most to you.
            </p>

            {/* Selection Card */}
            <div className="bg-neutral-50 border border-neutral-200 rounded-2xl p-6 sm:p-8 max-w-lg mx-auto">
              <h2 className="text-sm font-medium text-neutral-700 mb-4 text-left">Select your constituency</h2>
              
              <div className="space-y-3">
                {/* District Dropdown */}
                <div>
                  <label htmlFor="district-select" className="block text-xs text-neutral-500 mb-1 text-left">District</label>
                  <select
                    id="district-select"
                    value={selectedDistrict}
                    onChange={(e) => setSelectedDistrict(e.target.value)}
                    disabled={loading}
                    className="w-full px-3 py-2.5 bg-white border border-neutral-200 rounded-lg text-sm text-neutral-800 
                      focus:outline-none focus:ring-2 focus:ring-accent-500 focus:border-transparent
                      disabled:opacity-50 transition-all"
                  >
                    <option value="">All Districts</option>
                    {districts.map((d) => (
                      <option key={d.id} value={d.name}>{d.name}</option>
                    ))}
                  </select>
                </div>

                {/* Constituency Dropdown */}
                <div>
                  <label htmlFor="constituency-select" className="block text-xs text-neutral-500 mb-1 text-left">Constituency</label>
                  <select
                    id="constituency-select"
                    value={selectedConstituency}
                    onChange={(e) => setSelectedConstituency(e.target.value)}
                    disabled={!selectedDistrict}
                    className="w-full px-3 py-2.5 bg-white border border-neutral-200 rounded-lg text-sm text-neutral-800
                      focus:outline-none focus:ring-2 focus:ring-accent-500 focus:border-transparent
                      disabled:opacity-50 disabled:bg-neutral-100 transition-all"
                  >
                    <option value="">All Constituencies</option>
                    {constituencies.map((c) => (
                      <option key={c.id} value={c.name}>{c.name}</option>
                    ))}
                  </select>
                </div>

                <button
                  onClick={handleExplore}
                  className="w-full mt-2 px-4 py-2.5 bg-accent-600 text-white text-sm font-medium rounded-lg
                    hover:bg-accent-700 active:scale-[0.98] transition-all"
                >
                  Explore Candidates
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          {[
            {
              icon: (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              ),
              title: 'Candidate Profiles',
              desc: 'Education, criminal records, assets, and professional background sourced from official affidavits.',
            },
            {
              icon: (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              ),
              title: 'Compare Side by Side',
              desc: 'Place candidates next to each other and compare their backgrounds on every metric.',
            },
            {
              icon: (
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
                </svg>
              ),
              title: 'Dynamic Ranking',
              desc: 'Set your own priorities with sliders and see candidates ranked by what matters to you.',
            },
          ].map((f, i) => (
            <div key={i} className="bg-white border border-neutral-200 rounded-xl p-5 hover:border-neutral-300 transition-colors">
              <div className="w-9 h-9 rounded-lg bg-accent-50 text-accent-600 flex items-center justify-center mb-3">
                {f.icon}
              </div>
              <h3 className="font-medium text-neutral-900 text-sm mb-1">{f.title}</h3>
              <p className="text-neutral-500 text-xs leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
