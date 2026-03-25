import { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { fetchCandidates, fetchDistricts, fetchConstituencies } from '../api/client';
import CandidateCard from '../components/CandidateCard';

export default function CandidateList() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [candidates, setCandidates] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [constituencies, setConstituencies] = useState([]);
  const [district, setDistrict] = useState(searchParams.get('district') || '');
  const [constituency, setConstituency] = useState(searchParams.get('constituency') || '');
  const [loading, setLoading] = useState(true);
  const [compareList, setCompareList] = useState([]);

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

  useEffect(() => {
    setLoading(true);
    fetchCandidates({ district, constituency })
      .then(setCandidates)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [district, constituency]);

  const toggleCompare = (candidate) => {
    setCompareList((prev) => {
      const exists = prev.find((c) => c.id === candidate.id);
      if (exists) return prev.filter((c) => c.id !== candidate.id);
      if (prev.length >= 4) return prev;
      return [...prev, candidate];
    });
  };

  const goCompare = () => {
    const ids = compareList.map((c) => c.id).join(',');
    navigate(`/compare?ids=${ids}`);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
        <div>
          <h1 className="text-xl font-semibold text-neutral-900">Candidates</h1>
          <p className="text-sm text-neutral-500 mt-0.5">
            {loading ? 'Loading...' : `${candidates.length} candidates found`}
          </p>
        </div>

        {/* Compare bar */}
        {compareList.length > 0 && (
          <div className="flex items-center gap-3">
            <span className="text-xs text-neutral-500">{compareList.length}/4 selected</span>
            <button
              onClick={goCompare}
              disabled={compareList.length < 2}
              className="px-4 py-2 text-xs font-medium bg-accent-600 text-white rounded-lg 
                hover:bg-accent-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              Compare Selected
            </button>
            <button
              onClick={() => setCompareList([])}
              className="px-3 py-2 text-xs text-neutral-600 hover:text-neutral-900 transition-colors"
            >
              Clear
            </button>
          </div>
        )}
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <select
          value={district}
          onChange={(e) => { setDistrict(e.target.value); setConstituency(''); }}
          className="px-3 py-2 bg-white border border-neutral-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-accent-500"
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
          className="px-3 py-2 bg-white border border-neutral-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-accent-500 disabled:opacity-50"
        >
          <option value="">All Constituencies</option>
          {constituencies.map((c) => (
            <option key={c.id} value={c.name}>{c.name}</option>
          ))}
        </select>
      </div>

      {/* Grid */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="bg-white border border-neutral-200 rounded-xl p-5 animate-pulse">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-full bg-neutral-200"></div>
                <div className="flex-1">
                  <div className="h-4 bg-neutral-200 rounded w-2/3 mb-2"></div>
                  <div className="h-3 bg-neutral-100 rounded w-1/2"></div>
                </div>
              </div>
              <div className="space-y-2">
                <div className="h-3 bg-neutral-100 rounded"></div>
                <div className="h-3 bg-neutral-100 rounded w-3/4"></div>
              </div>
            </div>
          ))}
        </div>
      ) : candidates.length === 0 ? (
        <div className="text-center py-16">
          <p className="text-neutral-400 text-sm">No candidates found for the selected filters.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {candidates.map((candidate) => (
            <CandidateCard
              key={candidate.id}
              candidate={candidate}
              isSelected={compareList.some((c) => c.id === candidate.id)}
              onToggleCompare={() => toggleCompare(candidate)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
