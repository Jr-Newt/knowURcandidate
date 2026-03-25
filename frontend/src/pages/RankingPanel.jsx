import { useState, useEffect, useCallback } from 'react';
import { fetchRanking, fetchDistricts, fetchConstituencies } from '../api/client';
import Disclaimer from '../components/Disclaimer';
import { Link } from 'react-router-dom';

function formatCurrency(amount) {
  if (!amount) return '₹0';
  if (amount >= 10000000) return `₹${(amount / 10000000).toFixed(2)} Cr`;
  if (amount >= 100000) return `₹${(amount / 100000).toFixed(2)} L`;
  return `₹${amount.toLocaleString('en-IN')}`;
}

export default function RankingPanel() {
  const [weights, setWeights] = useState({
    education: 0.25,
    criminal: 0.25,
    experience: 0.25,
    assets: 0.25,
  });
  const [district, setDistrict] = useState('');
  const [constituency, setConstituency] = useState('');
  const [districts, setDistricts] = useState([]);
  const [constituencies, setConstituencies] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDistricts().then(setDistricts).catch(console.error);
  }, []);

  useEffect(() => {
    if (district) {
      fetchConstituencies(district).then(setConstituencies).catch(console.error);
    } else {
      setConstituencies([]);
      setConstituency('');
    }
  }, [district]);

  const doRank = useCallback(() => {
    setLoading(true);
    fetchRanking({ weights, district, constituency })
      .then(setResult)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [weights, district, constituency]);

  // Debounced ranking on weight change
  useEffect(() => {
    const timer = setTimeout(doRank, 300);
    return () => clearTimeout(timer);
  }, [doRank]);

  const updateWeight = (key, value) => {
    setWeights((prev) => ({ ...prev, [key]: parseFloat(value) }));
  };

  const totalWeight = weights.education + weights.criminal + weights.experience + weights.assets;

  const sliders = [
    { key: 'education', label: 'Education', desc: 'Higher → educated candidates rank higher', color: 'accent' },
    { key: 'criminal', label: 'Clean Record', desc: 'Higher → candidates with fewer cases rank higher', color: 'success' },
    { key: 'experience', label: 'Experience', desc: 'Higher → experienced candidates rank higher', color: 'warning' },
    { key: 'assets', label: 'Assets', desc: 'Higher → wealthier candidates rank higher', color: 'accent' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-xl font-semibold text-neutral-900">Dynamic Ranking</h1>
        <p className="text-sm text-neutral-500 mt-0.5">
          Adjust the sliders to rank candidates based on your priorities
        </p>
      </div>

      <Disclaimer />

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mt-6">
        {/* Controls Panel */}
        <div className="lg:col-span-4">
          <div className="bg-white border border-neutral-200 rounded-xl p-6 sticky top-20">
            {/* Filters */}
            <div className="mb-6">
              <h3 className="text-xs font-semibold text-neutral-700 uppercase tracking-wider mb-3">Filter</h3>
              <div className="space-y-2">
                <select
                  value={district}
                  onChange={(e) => { setDistrict(e.target.value); setConstituency(''); }}
                  className="w-full px-3 py-2 bg-neutral-50 border border-neutral-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-accent-500"
                >
                  <option value="">All Districts</option>
                  {districts.map((d) => (
                    <option key={d.id} value={d.name}>{d.name}</option>
                  ))}
                </select>
                <select
                  value={constituency}
                  onChange={(e) => setConstituency(e.target.value)}
                  disabled={!district}
                  className="w-full px-3 py-2 bg-neutral-50 border border-neutral-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-accent-500 disabled:opacity-50"
                >
                  <option value="">All Constituencies</option>
                  {constituencies.map((c) => (
                    <option key={c.id} value={c.name}>{c.name}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Sliders */}
            <div>
              <h3 className="text-xs font-semibold text-neutral-700 uppercase tracking-wider mb-3">Weights</h3>
              <div className="space-y-4">
                {sliders.map(({ key, label, desc }) => (
                  <div key={key}>
                    <div className="flex items-center justify-between mb-1">
                      <label className="text-sm font-medium text-neutral-700">{label}</label>
                      <span className="text-xs font-mono text-neutral-500">
                        {weights[key].toFixed(2)}
                        {totalWeight > 0 && (
                          <span className="text-neutral-400 ml-1">
                            ({Math.round((weights[key] / totalWeight) * 100)}%)
                          </span>
                        )}
                      </span>
                    </div>
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.05"
                      value={weights[key]}
                      onChange={(e) => updateWeight(key, e.target.value)}
                      className="w-full"
                    />
                    <p className="text-[10px] text-neutral-400 mt-0.5">{desc}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Quick presets */}
            <div className="mt-6 pt-4 border-t border-neutral-100">
              <p className="text-xs text-neutral-400 mb-2">Quick presets</p>
              <div className="flex flex-wrap gap-1.5">
                {[
                  { label: 'Equal', w: { education: 0.25, criminal: 0.25, experience: 0.25, assets: 0.25 } },
                  { label: 'Clean Record', w: { education: 0.1, criminal: 0.7, experience: 0.1, assets: 0.1 } },
                  { label: 'Education', w: { education: 0.7, criminal: 0.1, experience: 0.1, assets: 0.1 } },
                  { label: 'Experience', w: { education: 0.1, criminal: 0.1, experience: 0.7, assets: 0.1 } },
                ].map((preset) => (
                  <button
                    key={preset.label}
                    onClick={() => setWeights(preset.w)}
                    className="px-2.5 py-1 text-[10px] font-medium rounded-md border border-neutral-200 text-neutral-600 hover:bg-neutral-50 hover:border-neutral-300 transition-all"
                  >
                    {preset.label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Results */}
        <div className="lg:col-span-8">
          {loading && !result ? (
            <div className="space-y-3">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="bg-white border border-neutral-200 rounded-xl p-5 animate-pulse">
                  <div className="h-5 bg-neutral-200 rounded w-1/3 mb-2"></div>
                  <div className="h-3 bg-neutral-100 rounded w-1/2"></div>
                </div>
              ))}
            </div>
          ) : result && result.ranked_candidates?.length > 0 ? (
            <div className="space-y-3">
              {result.ranked_candidates.map((candidate, index) => (
                <div
                  key={candidate.id}
                  className={`bg-white border rounded-xl p-5 transition-all ${
                    index === 0 ? 'border-accent-200 ring-1 ring-accent-100' : 'border-neutral-200'
                  }`}
                >
                  <div className="flex items-start gap-4">
                    {/* Rank badge */}
                    <div className={`w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold shrink-0 ${
                      index === 0 ? 'bg-accent-100 text-accent-700' :
                      index === 1 ? 'bg-neutral-200 text-neutral-700' :
                      index === 2 ? 'bg-amber-100 text-amber-700' :
                      'bg-neutral-100 text-neutral-500'
                    }`}>
                      {index + 1}
                    </div>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <Link
                          to={`/candidate/${candidate.id}`}
                          className="font-medium text-neutral-900 hover:text-accent-600 transition-colors text-sm"
                        >
                          {candidate.name}
                        </Link>
                        <span className="text-xs px-1.5 py-0.5 rounded bg-neutral-100 text-neutral-600">
                          {candidate.party}
                        </span>
                      </div>
                      <p className="text-xs text-neutral-400">
                        {candidate.constituency_name}{candidate.district_name ? `, ${candidate.district_name}` : ''}
                        {candidate.age ? ` · Age ${candidate.age}` : ''}
                      </p>

                      {/* Score breakdown bar */}
                      <div className="mt-3 flex items-center gap-1">
                        <div className="flex h-2 flex-1 rounded-full overflow-hidden bg-neutral-100">
                          <div className="bg-blue-400 transition-all duration-300" style={{ width: `${candidate.breakdown.education * 100}%` }} title="Education"></div>
                          <div className="bg-green-400 transition-all duration-300" style={{ width: `${candidate.breakdown.criminal * 100}%` }} title="Criminal"></div>
                          <div className="bg-amber-400 transition-all duration-300" style={{ width: `${candidate.breakdown.experience * 100}%` }} title="Experience"></div>
                          <div className="bg-purple-400 transition-all duration-300" style={{ width: `${candidate.breakdown.assets * 100}%` }} title="Assets"></div>
                        </div>
                        <span className="text-xs font-mono font-semibold text-neutral-700 w-12 text-right">
                          {(candidate.total_score * 100).toFixed(1)}
                        </span>
                      </div>

                      {/* Breakdown detail */}
                      <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-[10px] text-neutral-400">
                        <span><span className="inline-block w-2 h-2 rounded-sm bg-blue-400 mr-1"></span>Edu {(candidate.breakdown.education * 100).toFixed(1)}</span>
                        <span><span className="inline-block w-2 h-2 rounded-sm bg-green-400 mr-1"></span>Crim {(candidate.breakdown.criminal * 100).toFixed(1)}</span>
                        <span><span className="inline-block w-2 h-2 rounded-sm bg-amber-400 mr-1"></span>Exp {(candidate.breakdown.experience * 100).toFixed(1)}</span>
                        <span><span className="inline-block w-2 h-2 rounded-sm bg-purple-400 mr-1"></span>Assets {(candidate.breakdown.assets * 100).toFixed(1)}</span>
                      </div>
                    </div>

                    {/* Key metrics */}
                    <div className="hidden sm:flex flex-col items-end gap-1 text-xs text-neutral-500 shrink-0">
                      <span>{candidate.education}</span>
                      <span>{candidate.criminal_cases} cases</span>
                      <span>{formatCurrency(candidate.assets)}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-16">
              <p className="text-neutral-400 text-sm">No candidates found. Try adjusting your filters.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
