<?php

namespace App\Http\Controllers;

use App\Helpers\Image;
use Illuminate\Http\Request;
use Illuminate\Support\Str;

class WelcomeController extends Controller
{
    public function index(Request $request, Image $image)
    {
        $selected = null;
        $images = null;

        if ($request->has('selected')) {
            $selectedImageName = $request->input('selected');
            $file = $image->getImageFile($selectedImageName);

            $selected = [
                'name' => $selectedImageName,
                'base64' => Str::toBase64($file),
            ];

            $images = $image->getSimilerImages($selectedImageName);
        } else {
            $images = $image->getRandomImages(50);
        }

        return view('welcome', [
            'selected' => $selected,
            'images' => $images,
        ]);
    }
}
