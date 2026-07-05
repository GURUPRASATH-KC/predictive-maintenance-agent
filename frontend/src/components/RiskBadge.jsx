const styles = {
  Normal: 'badge-normal',
  Warning: 'badge-warning',
  Critical: 'badge-critical',
}

export default function RiskBadge({ level }) {
  return (
    <span className={`inline-flex items-center px-2.5 py-1 rounded-md text-xs font-semibold ${styles[level] || styles.Normal}`}>
      {level}
    </span>
  )
}
