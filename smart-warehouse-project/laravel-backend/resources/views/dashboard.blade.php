<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Warehouse Dashboard</title>
    {{-- Using Tailwind's Play CDN for rapid development --}}
    <script src="https://cdn.tailwindcss.com"></script>
    {{-- Using Font Awesome for icons --}}
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

</head>
<body class="bg-slate-900 text-slate-300 font-sans">

    <div id="app-container" class="flex flex-col min-h-screen">

        {{-- Header Section --}}
        <header class="bg-slate-800 shadow-lg border-b border-slate-700 sticky top-0 z-10">
            <nav class="container mx-auto px-6 py-4">
                <div class="flex items-center justify-between">
                    {{-- App Branding --}}
                    <div class="text-white font-bold text-2xl">
                        <a href="#" class="flex items-center">
                            <i class="fas fa-warehouse mr-3 text-blue-400"></i>
                            <span>Thumbworx</span>
                        </a>
                    </div>
                    {{-- Primary Navigation --}}
                    <div class="hidden md:flex items-center space-x-8">
                        <a href="#" class="text-white font-semibold border-b-2 border-blue-500 pb-1">Analytics Dashboard</a>
                        <a href="#" class="text-slate-300 hover:text-blue-400 transition-colors duration-300">Inventory Logs</a>
                        <a href="#" class="text-slate-300 hover:text-blue-400 transition-colors duration-300">System Status</a>
                    </div>
                    {{-- User Profile Area --}}
                    <div class="hidden md:flex items-center">
                        <span class="text-slate-400 mr-4">Welcome, Warehouse Manager</span>
                        <img class="h-10 w-10 rounded-full object-cover" src="https://i.pravatar.cc/150?u=manager" alt="User avatar">
                    </div>
                    {{-- Mobile Menu Button --}}
                    <div class="md:hidden">
                        <button class="text-white focus:outline-none">
                            <i class="fas fa-bars"></i>
                        </button>
                    </div>
                </div>
            </nav>
        </header>

        {{-- Main Content Section --}}
        <main class="container mx-auto px-6 py-8 flex-grow">

            {{-- Page Title and Live Indicator --}}
            <div class="flex items-center justify-between mb-8">
                <h1 class="text-4xl font-bold text-white">Live Operations Dashboard</h1>
                <div class="flex items-center text-sm bg-green-500/20 text-green-400 px-3 py-1 rounded-full">
                    <i class="fas fa-circle mr-2 text-xs animate-pulse"></i>
                    <span>Live Data Feed</span>
                </div>
            </div>

            {{-- KPI Stat Cards (Updated for Warehouse Metrics) --}}
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <!-- Card 1: Total Stock -->
                <div class="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700">
                    <div class="flex items-center">
                        <div class="bg-green-500/20 p-3 rounded-full">
                            <i class="fas fa-boxes-stacked text-xl text-green-400"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm text-slate-400">Total Items in Stock</p>
                            <p class="text-3xl font-bold text-white">14,289</p>
                        </div>
                    </div>
                </div>
                <!-- Card 2: Items Out (24h) -->
                <div class="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700">
                    <div class="flex items-center">
                        <div class="bg-orange-500/20 p-3 rounded-full">
                            <i class="fas fa-truck-fast text-xl text-orange-400"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm text-slate-400">Items Shipped (24h)</p>
                            <p class="text-3xl font-bold text-white">1,302</p>
                        </div>
                    </div>
                </div>
                <!-- Card 3: Items In (24h) -->
                <div class="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700">
                    <div class="flex items-center">
                        <div class="bg-blue-500/20 p-3 rounded-full">
                            <i class="fas fa-dolly text-xl text-blue-400"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm text-slate-400">Items Received (24h)</p>
                            <p class="text-3xl font-bold text-white">2,510</p>
                        </div>
                    </div>
                </div>
                <!-- Card 4: Products Tracked -->
                <div class="bg-slate-800 p-6 rounded-xl shadow-lg border border-slate-700">
                    <div class="flex items-center">
                        <div class="bg-purple-500/20 p-3 rounded-full">
                            <i class="fas fa-barcode text-xl text-purple-400"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-sm text-slate-400">Unique Products (SKUs)</p>
                            <p class="text-3xl font-bold text-white">{{ $uniqueSkuCount ?? 100 }}</p> {{-- Example of dynamic data --}}
                        </div>
                    </div>
                </div>
            </div>

            {{-- Iframe Container --}}
            <div class="bg-slate-800 rounded-xl shadow-2xl overflow-hidden border border-slate-700">
                <div class="p-6 border-b border-slate-700">
                    <h2 class="text-xl font-semibold text-white">Metabase Warehouse Overview</h2>
                    <p class="text-sm text-slate-400 mt-1">
                        Live inventory analysis. Use the filters within the dashboard to drill down into specific data points.
                    </p>
                </div>
                
                {{-- This is where the Metabase dashboard is embedded --}}
                <div class="p-2 bg-slate-900">
                    <iframe
                        src="http://localhost:3030/public/dashboard/b361e2e0-48e7-4a4e-9002-174b8e887d56"
                        frameborder="0"
                        width="100%"
                        height="800"
                        allowtransparency
                        class="rounded-lg"
                    ></iframe>
                </div>
            </div>
        </main>

        {{-- Footer Section --}}
        <footer class="mt-12">
            <div class="text-center py-6 text-slate-500 text-sm border-t border-slate-800">
                &copy; {{ date('Y') }} Smart Warehouse Inc. All Rights Reserved. Powered by Laravel & Metabase.
            </div>
        </footer>

    </div>
</body>
</html>