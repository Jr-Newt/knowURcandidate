import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchCandidate, fetchCandidateNews } from '../api/client';
import NewsCard from '../components/NewsCard';
import RedFlag from '../components/RedFlag';

function formatCurrency(amount) {
  if (!amount) return '₹0';
  if (amount >= 10000000) return `₹${(amount / 10000000).toFixed(2)} Cr`;
  if (amount >= 100000) return `₹${(amount / 100000).toFixed(2)} L`;
  return `₹${amount.toLocaleString('en-IN')}`;
}

function ScoreBar({ label, score, color = 'accent' }) {
  const pct = Math.round(score * 100);
  const colorMap = {
    accent: 'bg-accent-500',
    success: 'bg-success-500',
    danger: 'bg-danger-500',
    warning: 'bg-warning-500',
  };
  return (
    <div className="flex items-center gap-3">
      <span className="text-xs text-neutral-500 w-24 shrink-0">{label}</span>
      <div className="flex-1 h-2 bg-neutral-100 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${colorMap[color]}`} style={{ width: `${pct}%` }}></div>
      </div>
      <span className="text-xs font-medium text-neutral-700 w-10 text-right">{pct}%</span>
    </div>
  );
}

export default function CandidateDetail() {
  const { id } = useParams();
  const [candidate, setCandidate] = useState(null);
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([fetchCandidate(id), fetchCandidateNews(id)])
      .then(([c, n]) => { setCandidate(c); setNews(n); })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="animate-pulse space-y-6">
          <div className="h-6 bg-neutral-200 rounded w-1/3"></div>
          <div className="h-4 bg-neutral-100 rounded w-1/4"></div>
          <div className="h-48 bg-neutral-100 rounded-xl"></div>
        </div>
      </div>
    );
  }

  if (!candidate) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center">
        <p className="text-neutral-400">Candidate not found.</p>
        <Link to="/candidates" className="text-accent-600 text-sm mt-2 inline-block hover:underline">← Back to candidates</Link>
      </div>
    );
  }

  const hasRedFlags = candidate.criminal_cases > 0 || candidate.serious_cases > 0 ||
    (candidate.assets > 100000000);

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Breadcrumb */}
      <nav className="text-xs text-neutral-400 mb-6">
        <Link to="/candidates" className="hover:text-neutral-600 transition-colors">Candidates</Link>
        <span className="mx-2">›</span>
        <span className="text-neutral-600">{candidate.name}</span>
      </nav>

      {/* Profile Header */}
      <div className="bg-white border border-neutral-200 rounded-xl p-6 sm:p-8 mb-6">
        <div className="flex flex-col sm:flex-row sm:items-start gap-4">
          {/* Avatar */}
          <div className="w-16 h-16 rounded-full bg-accent-100 text-accent-700 flex items-center justify-center text-xl font-bold shrink-0">
            {candidate.name.split(' ').map(n => n[0]).join('').slice(0, 2)}
          </div>
          <div className="flex-1">
            <h1 className="text-xl font-semibold text-neutral-900">{candidate.name}</h1>
            <div className="flex flex-wrap items-center gap-2 mt-1">
              <span className="inline-flex items-center px-2 py-0.5 rounded-md bg-neutral-100 text-neutral-700 text-xs font-medium">
                {candidate.party}
              </span>
              <span className="text-xs text-neutral-400">
                {candidate.constituency_name}, {candidate.district_name}
              </span>
            </div>
            {candidate.age && (
              <p className="text-xs text-neutral-500 mt-2">Age: {candidate.age} · {candidate.profession}</p>
            )}
          </div>
          {candidate.affidavit_link && (
            <a
              href={candidate.affidavit_link}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs text-accent-600 hover:text-accent-700 hover:underline shrink-0"
            >
              View Affidavit ↗
            </a>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left column — details */}
        <div className="lg:col-span-2 space-y-6">
          {/* Red Flags */}
          {hasRedFlags && (
            <div className="space-y-2">
              {candidate.criminal_cases > 0 && (
                <RedFlag
                  type="criminal"
                  title={`${candidate.criminal_cases} criminal case${candidate.criminal_cases > 1 ? 's' : ''} declared`}
                  subtitle={candidate.serious_cases > 0 ? `${candidate.serious_cases} serious/heinous case(s)` : 'No serious cases'}
                />
              )}
              {candidate.assets > 100000000 && (
                <RedFlag
                  type="wealth"
                  title={`Declared assets: ${formatCurrency(candidate.assets)}`}
                  subtitle="Unusually high asset declaration"
                />
              )}
            </div>
          )}

          {/* Background Info */}
          <div className="bg-white border border-neutral-200 rounded-xl p-6">
            <h2 className="text-sm font-semibold text-neutral-900 mb-4">Background</h2>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-neutral-400 text-xs">Education</span>
                <p className="text-neutral-800 font-medium">{candidate.education || 'Not declared'}</p>
              </div>
              <div>
                <span className="text-neutral-400 text-xs">Profession</span>
                <p className="text-neutral-800 font-medium">{candidate.profession || 'Not declared'}</p>
              </div>
              <div>
                <span className="text-neutral-400 text-xs">Total Assets</span>
                <p className="text-neutral-800 font-medium">{formatCurrency(candidate.assets)}</p>
              </div>
              <div>
                <span className="text-neutral-400 text-xs">Liabilities</span>
                <p className="text-neutral-800 font-medium">{formatCurrency(candidate.liabilities)}</p>
              </div>
              <div>
                <span className="text-neutral-400 text-xs">Criminal Cases</span>
                <p className="text-neutral-800 font-medium">{candidate.criminal_cases}</p>
              </div>
              <div>
                <span className="text-neutral-400 text-xs">Serious Cases</span>
                <p className="text-neutral-800 font-medium">{candidate.serious_cases}</p>
              </div>
            </div>
          </div>

          {/* News */}
          <div>
            <h2 className="text-sm font-semibold text-neutral-900 mb-3">Recent News</h2>
            {news.length === 0 ? (
              <p className="text-xs text-neutral-400">No news articles found for this candidate.</p>
            ) : (
              <div className="space-y-3">
                {news.map((article) => (
                  <NewsCard key={article.id} article={article} />
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right column — scores */}
        <div>
          <div className="bg-white border border-neutral-200 rounded-xl p-6 sticky top-20">
            <h2 className="text-sm font-semibold text-neutral-900 mb-4">Normalized Scores</h2>
            <div className="space-y-3">
              <ScoreBar label="Education" score={candidate.education_score} color="accent" />
              <ScoreBar label="Criminal" score={candidate.criminal_score} color={candidate.criminal_score >= 0.7 ? 'success' : 'danger'} />
              <ScoreBar label="Experience" score={candidate.experience_score} color="accent" />
              <ScoreBar label="Assets" score={candidate.asset_score} color="warning" />
            </div>
            <p className="text-[10px] text-neutral-400 mt-4 leading-relaxed">
              Scores are normalized 0–1. Criminal score: higher = fewer cases. 
              Data sourced from election affidavits.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
