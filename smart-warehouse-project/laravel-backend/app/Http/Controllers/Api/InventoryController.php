<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class InventoryController extends Controller
{
    public function index()
    {
        // Query the new table and join to get product details
        $transactions = DB::table('inventory_transactions')
            ->join('products', 'inventory_transactions.product_id', '=', 'products.id')
            ->select(
                'inventory_transactions.id',
                'products.sku',
                'products.name as product_name', // Alias for frontend compatibility
                'inventory_transactions.quantity',
                'inventory_transactions.status',
                'inventory_transactions.scanned_at as last_scanned' // Alias for frontend
            )
            ->orderBy('scanned_at', 'desc')
            ->get();

        return response()->json($transactions);
    }

    public function store(Request $request)
    {
        $validatedData = $request->validate([
            'sku' => 'required|string|max:20',
            'product_name' => 'required|string',
            'quantity' => 'required|integer',
            'status' => 'required|in:IN,OUT',
        ]);

        $scannerUrl = env('FLASK_SCANNER_URL');
        $response = Http::post($scannerUrl, $validatedData);

        if ($response->successful()) {
            return response()->json(['message' => 'Scan data forwarded successfully'], 201);
        } else {
            Log::error('Flask scanner service failed.', [
                'status' => $response->status(),
                'body' => $response->body()
            ]);
            return response()->json(['error' => 'Failed to forward scan data'], $response->status());
        }
    }
}
