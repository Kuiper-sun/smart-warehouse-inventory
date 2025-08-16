<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('locations', function (Blueprint $table) {
            $table->id();
            $table->integer('aisle');
            $table->char('shelf', 1);
            $table->integer('bin');
            $table->text('description')->nullable();
            $table->unique(['aisle', 'shelf', 'bin']); // Ensure location is unique
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('locations');
    }
};