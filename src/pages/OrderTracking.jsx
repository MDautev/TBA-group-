export function OrderTracking({ user }) {
    return (
      <div className="p-8">
        <h2 className="text-2xl">Order Tracking</h2>
        {user ? (
          <p>Tracking details will be shown here.</p>
        ) : (
          <p>Please log in to track your orders.</p>
        )}
      </div>
    );
  }
  