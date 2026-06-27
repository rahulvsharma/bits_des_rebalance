import React, { useState } from "react";
import axios from "axios";

interface Asset {
  symbol: string;
  current_allocation: number;
  target_allocation: number;
}

export const RebalancingComponent: React.FC = () => {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [actions, setActions] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleRebalance = async () => {
    setLoading(true);
    try {
      const response = await axios.post("/api/rebalance/calculate", {
        user_id: "user-001",
        assets: assets,
      });
      setActions(response.data.actions);
    } catch (error) {
      console.error("Rebalancing error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="rebalancing p-6">
      <h1 className="text-2xl font-bold mb-4">Portfolio Rebalancing</h1>
      <button
        onClick={handleRebalance}
        disabled={loading}
        className="bg-green-500 text-white px-4 py-2 rounded"
      >
        {loading ? "Calculating..." : "Calculate Rebalance"}
      </button>

      {actions.length > 0 && (
        <div className="mt-6">
          <h2 className="font-bold mb-2">Recommended Actions:</h2>
          {actions.map((action, idx) => (
            <div
              key={idx}
              className={`p-3 rounded mb-2 ${action.action === "buy" ? "bg-green-100" : "bg-red-100"}`}
            >
              <p>
                {action.symbol}: {action.action.toUpperCase()}{" "}
                {Math.abs(action.change_percent).toFixed(1)}%
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RebalancingComponent;
