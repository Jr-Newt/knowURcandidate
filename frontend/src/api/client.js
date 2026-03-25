import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || '/api';

const client = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ─── Districts ───
export const fetchDistricts = async () => {
  const { data } = await client.get('/districts');
  return data.districts;
};

// ─── Constituencies ───
export const fetchConstituencies = async (district) => {
  const { data } = await client.get('/constituencies', {
    params: { district },
  });
  return data.constituencies;
};

// ─── Candidates ───
export const fetchCandidates = async ({ district, constituency } = {}) => {
  const params = {};
  if (district) params.district = district;
  if (constituency) params.constituency = constituency;
  const { data } = await client.get('/candidates', { params });
  return data.candidates;
};

export const fetchCandidate = async (id) => {
  const { data } = await client.get(`/candidate/${id}`);
  return data.candidate;
};

export const fetchCandidateNews = async (id) => {
  const { data } = await client.get(`/candidate/${id}/news`);
  return data.news;
};

// ─── Ranking ───
export const fetchRanking = async ({ weights, district, constituency }) => {
  const { data } = await client.post('/rank', {
    weights,
    district: district || null,
    constituency: constituency || null,
  });
  return data;
};

export default client;
