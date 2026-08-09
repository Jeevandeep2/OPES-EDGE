const domainData = {
  healthcare: {
    name: 'Healthcare Services',
    slug: 'healthcare',
    summary: 'Clear health information, wellness guidance, and service discovery for more informed care.',
    image: 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1600&q=82',
    imageAlt: 'Healthcare professional in a bright clinic',
    demoLabel: 'Informational foundation',
    features: [
      { title: 'Wellness check-in', text: 'Track simple habits such as water, movement, sleep, and meditation.', icon: 'bi-heart-pulse' },
      { title: 'Find a doctor', text: 'A directory-ready space for verified doctor profiles and appointment links.', icon: 'bi-person-vcard' },
      { title: 'Preliminary symptom information', text: 'Educational guidance only. Consult a qualified healthcare professional for care.', icon: 'bi-clipboard2-pulse' },
    ],
    actions: [
      { label: 'Open symptom information', href: '/healthcare/symptom-checker', icon: 'bi-clipboard2-pulse' },
      { label: 'Browse doctor directory', href: '/healthcare/doctor-directory', icon: 'bi-person-vcard' },
    ],
    note: 'This module does not diagnose conditions, prescribe medicines, or replace a doctor. Any health information shown is preliminary and educational.',
  },
  community: {
    name: 'Community Services & Development',
    slug: 'community',
    summary: 'Simple access to civic information, local notices, and practical digital-service guidance.',
    image: 'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&w=1600&q=82',
    imageAlt: 'Community members standing together outdoors',
    demoLabel: 'Official-link ready',
    features: [
      { title: 'Government services', text: 'Start with official links for identity, documents, scholarships, and citizen services.', icon: 'bi-bank' },
      { title: 'Community notices', text: 'A clear home for Gram Panchayat notices, deadlines, and local announcements.', icon: 'bi-megaphone' },
      { title: 'Digital access help', text: 'Plain-language guidance for smartphones, online payments, and public services.', icon: 'bi-phone' },
    ],
    actions: [
      { label: 'Open community notices', href: '/community/events', icon: 'bi-megaphone' },
      { label: 'View service feedback', href: '/community/feedback', icon: 'bi-chat-square-text' },
    ],
    links: [
      { label: 'Aadhaar', href: 'https://uidai.gov.in/' },
      { label: 'DigiLocker', href: 'https://www.digilocker.gov.in/' },
      { label: 'Voter services', href: 'https://voters.eci.gov.in/' },
      { label: 'National scholarship portal', href: 'https://scholarships.gov.in/' },
    ],
    note: 'Government links open official websites. OPES EDGE does not claim government affiliation or process applications on the user’s behalf.',
  },
  energy: {
    name: 'Energy Management',
    slug: 'energy',
    summary: 'Understand consumption, solar potential, and practical ways to reduce energy waste.',
    image: 'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=1600&q=82',
    imageAlt: 'Wind turbines in a field at sunset',
    demoLabel: 'Simulated sensor data',
    metrics: [
      { label: "Today's consumption", value: '8.4 kWh', detail: 'Demo reading' },
      { label: 'Solar generation', value: '4.1 kWh', detail: 'Demo reading' },
      { label: 'Usage alert', value: 'Low', detail: 'No simulated alert' },
    ],
    features: [
      { title: 'Usage monitoring', text: 'Ready for voltage, current, power, energy, date, and time readings from a future device feed.', icon: 'bi-lightning-charge' },
      { title: 'Carbon footprint', text: 'Use consumption records as the foundation for an energy-saving estimate.', icon: 'bi-cloud-sun' },
      { title: 'Smart appliance controls', text: 'Integration-ready interface for devices once a secure IoT service is connected.', icon: 'bi-plug' },
    ],
    actions: [
      { label: 'Open energy monitoring', href: '/energy/monitoring', icon: 'bi-graph-up' },
    ],
    note: 'The values on this page are simulated demo data. No ESP32, ACS712, voltage, or temperature sensor is connected to this project yet.',
  },
  water: {
    name: 'Water Management',
    slug: 'water',
    summary: 'Monitor shared water resources and make conservation easier to understand.',
    image: 'https://images.unsplash.com/photo-1538300342682-cf57afb97285?auto=format&fit=crop&w=1600&q=82',
    imageAlt: 'Clear blue water flowing over stones',
    demoLabel: 'Simulated monitoring data',
    metrics: [
      { label: 'Tank level', value: '72%', detail: 'Demo reading' },
      { label: 'Daily usage', value: '410 L', detail: 'Demo reading' },
      { label: 'Leak status', value: 'Clear', detail: 'No simulated alert' },
    ],
    features: [
      { title: 'Water level and flow', text: 'Ready for water-level, flow-rate, and time-series readings from a future sensor feed.', icon: 'bi-droplet-half' },
      { title: 'Rainwater and greywater', text: 'Track stored rainwater and reused greywater once household records are connected.', icon: 'bi-cloud-rain' },
      { title: 'Leak awareness', text: 'A clear alert surface for leak, overflow, and low-level events.', icon: 'bi-exclamation-triangle' },
    ],
    actions: [
      { label: 'Open water monitoring', href: '/water/monitoring', icon: 'bi-graph-up' },
    ],
    note: 'The values on this page are simulated demo data. No water-flow, water-level, or soil-moisture sensor is connected to this project yet.',
  },
};

function getDomain(domain) {
  return domainData[domain];
}

module.exports = { getDomain };