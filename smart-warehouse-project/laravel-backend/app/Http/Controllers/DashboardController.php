<?php
// File: laravel-backend/app/Http/Controllers/DashboardController.php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\View\View;

class DashboardController extends Controller
{
    /**
     * Display the main analytics dashboard.
     */
    public function index(): View
    {
        return view('dashboard');
    }
}