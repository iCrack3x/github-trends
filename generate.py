#!/usr/bin/env python3
"""
GitHub Trends Analyzer MVP
Aggregates trending repositories and generates SEO-optimized static pages.
"""

import json
import os
import random
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# Configuration
OUTPUT_DIR = "output"
REPOS_DIR = os.path.join(OUTPUT_DIR, "repos")
CATEGORIES_DIR = os.path.join(OUTPUT_DIR, "categories")
GITHUB_API_BASE = "https://api.github.com"

def ensure_dirs():
    """Create output directories if they don't exist."""
    os.makedirs(REPOS_DIR, exist_ok=True)
    os.makedirs(CATEGORIES_DIR, exist_ok=True)

def fetch_trending_repos() -> List[Dict[str, Any]]:
    """Fetch trending repositories from GitHub."""
    # Try to fetch real data, fallback to mock data
    try:
        # Search for recently created repos with most stars
        query = "created:>" + (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        url = f"{GITHUB_API_BASE}/search/repositories?q={query}&sort=stars&order=desc&per_page=50"
        
        req = Request(url, headers={
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Trends-Analyzer"
        })
        
        with urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            return data.get("items", [])
    except (HTTPError, Exception) as e:
        print(f"Could not fetch from API: {e}")
        print("Using mock data instead...")
        return get_mock_data()

def get_mock_data() -> List[Dict[str, Any]]:
    """Generate realistic mock data for MVP demonstration."""
    mock_repos = [
        {
            "id": 1,
            "name": "awesome-ai-assistant",
            "full_name": "johndoe/awesome-ai-assistant",
            "description": "A powerful AI assistant framework with built-in RAG capabilities, supporting multiple LLM providers and custom tool integrations.",
            "html_url": "https://github.com/johndoe/awesome-ai-assistant",
            "stargazers_count": 12500,
            "language": "Python",
            "forks_count": 890,
            "open_issues_count": 45,
            "topics": ["ai", "llm", "rag", "assistant", "openai"],
            "created_at": "2025-01-15T10:00:00Z",
            "updated_at": "2025-01-28T15:30:00Z",
            "owner": {"login": "johndoe", "avatar_url": "https://avatars.githubusercontent.com/u/1"}
        },
        {
            "id": 2,
            "name": "rust-wasm-runtime",
            "full_name": "rustacean/rust-wasm-runtime",
            "description": "High-performance WebAssembly runtime written in Rust with WASI support and minimal overhead.",
            "html_url": "https://github.com/rustacean/rust-wasm-runtime",
            "stargazers_count": 9800,
            "language": "Rust",
            "forks_count": 560,
            "open_issues_count": 23,
            "topics": ["wasm", "webassembly", "runtime", "wasi", "rust"],
            "created_at": "2025-01-10T08:00:00Z",
            "updated_at": "2025-01-27T12:00:00Z",
            "owner": {"login": "rustacean", "avatar_url": "https://avatars.githubusercontent.com/u/2"}
        },
        {
            "id": 3,
            "name": "nextjs-dashboard-kit",
            "full_name": "webdev/nextjs-dashboard-kit",
            "description": "Production-ready dashboard starter with Next.js 14, Tailwind CSS, Prisma, and NextAuth. Includes 20+ UI components.",
            "html_url": "https://github.com/webdev/nextjs-dashboard-kit",
            "stargazers_count": 15400,
            "language": "TypeScript",
            "forks_count": 1200,
            "open_issues_count": 67,
            "topics": ["nextjs", "react", "dashboard", "tailwindcss", "prisma"],
            "created_at": "2025-01-05T14:00:00Z",
            "updated_at": "2025-01-28T09:00:00Z",
            "owner": {"login": "webdev", "avatar_url": "https://avatars.githubusercontent.com/u/3"}
        },
        {
            "id": 4,
            "name": "go-microservices-framework",
            "full_name": "godev/go-microservices-framework",
            "description": "Lightweight microservices framework for Go with built-in service discovery, load balancing, and circuit breaker patterns.",
            "html_url": "https://github.com/godev/go-microservices-framework",
            "stargazers_count": 8200,
            "language": "Go",
            "forks_count": 430,
            "open_issues_count": 34,
            "topics": ["go", "golang", "microservices", "framework", "grpc"],
            "created_at": "2025-01-12T11:00:00Z",
            "updated_at": "2025-01-28T16:00:00Z",
            "owner": {"login": "godev", "avatar_url": "https://avatars.githubusercontent.com/u/4"}
        },
        {
            "id": 5,
            "name": "react-native-ui-lib",
            "full_name": "mobiledev/react-native-ui-lib",
            "description": "Comprehensive UI library for React Native with 50+ components, animations, and theming support.",
            "html_url": "https://github.com/mobiledev/react-native-ui-lib",
            "stargazers_count": 6700,
            "language": "TypeScript",
            "forks_count": 380,
            "open_issues_count": 29,
            "topics": ["react-native", "mobile", "ui", "components", "typescript"],
            "created_at": "2025-01-08T09:00:00Z",
            "updated_at": "2025-01-27T14:00:00Z",
            "owner": {"login": "mobiledev", "avatar_url": "https://avatars.githubusercontent.com/u/5"}
        },
        {
            "id": 6,
            "name": "ml-pipeline-tools",
            "full_name": "mlengineer/ml-pipeline-tools",
            "description": "End-to-end ML pipeline management with experiment tracking, model versioning, and deployment automation.",
            "html_url": "https://github.com/mlengineer/ml-pipeline-tools",
            "stargazers_count": 5400,
            "language": "Python",
            "forks_count": 290,
            "open_issues_count": 18,
            "topics": ["machine-learning", "mlops", "pipeline", "experiment-tracking", "python"],
            "created_at": "2025-01-03T16:00:00Z",
            "updated_at": "2025-01-26T11:00:00Z",
            "owner": {"login": "mlengineer", "avatar_url": "https://avatars.githubusercontent.com/u/6"}
        },
        {
            "id": 7,
            "name": "sveltekit-ecommerce",
            "full_name": "sveltefan/sveltekit-ecommerce",
            "description": "Full-stack e-commerce solution built with SvelteKit, featuring cart, checkout, admin panel, and Stripe integration.",
            "html_url": "https://github.com/sveltefan/sveltekit-ecommerce",
            "stargazers_count": 4300,
            "language": "TypeScript",
            "forks_count": 210,
            "open_issues_count": 15,
            "topics": ["svelte", "sveltekit", "ecommerce", "stripe", "typescript"],
            "created_at": "2025-01-14T13:00:00Z",
            "updated_at": "2025-01-28T10:00:00Z",
            "owner": {"login": "sveltefan", "avatar_url": "https://avatars.githubusercontent.com/u/7"}
        },
        {
            "id": 8,
            "name": "kubernetes-operator-sdk",
            "full_name": "k8sdev/kubernetes-operator-sdk",
            "description": "Simplified SDK for building Kubernetes operators with minimal boilerplate and built-in best practices.",
            "html_url": "https://github.com/k8sdev/kubernetes-operator-sdk",
            "stargazers_count": 7200,
            "language": "Go",
            "forks_count": 340,
            "open_issues_count": 28,
            "topics": ["kubernetes", "operator", "k8s", "go", "devops"],
            "created_at": "2025-01-11T07:00:00Z",
            "updated_at": "2025-01-28T08:00:00Z",
            "owner": {"login": "k8sdev", "avatar_url": "https://avatars.githubusercontent.com/u/8"}
        },
        {
            "id": 9,
            "name": "fastapi-starter-template",
            "full_name": "pythonista/fastapi-starter-template",
            "description": "Complete FastAPI project template with authentication, database integration, caching, and deployment configs.",
            "html_url": "https://github.com/pythonista/fastapi-starter-template",
            "stargazers_count": 8900,
            "language": "Python",
            "forks_count": 620,
            "open_issues_count": 42,
            "topics": ["fastapi", "python", "api", "template", "backend"],
            "created_at": "2025-01-06T10:00:00Z",
            "updated_at": "2025-01-28T13:00:00Z",
            "owner": {"login": "pythonista", "avatar_url": "https://avatars.githubusercontent.com/u/9"}
        },
        {
            "id": 10,
            "name": "vue-dashboard-pro",
            "full_name": "vuejsfan/vue-dashboard-pro",
            "description": "Professional Vue 3 dashboard template with Vite, Pinia, and comprehensive charting library integration.",
            "html_url": "https://github.com/vuejsfan/vue-dashboard-pro",
            "stargazers_count": 5100,
            "language": "Vue",
            "forks_count": 280,
            "open_issues_count": 22,
            "topics": ["vue", "vue3", "dashboard", "vite", "frontend"],
            "created_at": "2025-01-09T15:00:00Z",
            "updated_at": "2025-01-27T16:00:00Z",
            "owner": {"login": "vuejsfan", "avatar_url": "https://avatars.githubusercontent.com/u/10"}
        },
        {
            "id": 11,
            "name": "blockchain-rust-node",
            "full_name": "cryptodev/blockchain-rust-node",
            "description": "Educational blockchain implementation in Rust with Proof of Stake consensus and smart contract support.",
            "html_url": "https://github.com/cryptodev/blockchain-rust-node",
            "stargazers_count": 4600,
            "language": "Rust",
            "forks_count": 390,
            "open_issues_count": 31,
            "topics": ["blockchain", "rust", "cryptocurrency", "pos", "smart-contracts"],
            "created_at": "2025-01-13T12:00:00Z",
            "updated_at": "2025-01-28T11:00:00Z",
            "owner": {"login": "cryptodev", "avatar_url": "https://avatars.githubusercontent.com/u/11"}
        },
        {
            "id": 12,
            "name": "threejs-experiments",
            "full_name": "webglartist/threejs-experiments",
            "description": "Collection of stunning Three.js experiments, shaders, and interactive 3D web experiences.",
            "html_url": "https://github.com/webglartist/threejs-experiments",
            "stargazers_count": 3800,
            "language": "JavaScript",
            "forks_count": 450,
            "open_issues_count": 12,
            "topics": ["threejs", "webgl", "3d", "shaders", "javascript"],
            "created_at": "2025-01-04T08:00:00Z",
            "updated_at": "2025-01-26T09:00:00Z",
            "owner": {"login": "webglartist", "avatar_url": "https://avatars.githubusercontent.com/u/12"}
        },
        {
            "id": 13,
            "name": "flutter-state-management",
            "full_name": "flutterdev/flutter-state-management",
            "description": "Comprehensive comparison and examples of all Flutter state management solutions: Riverpod, Bloc, GetX, and more.",
            "html_url": "https://github.com/flutterdev/flutter-state-management",
            "stargazers_count": 6200,
            "language": "Dart",
            "forks_count": 510,
            "open_issues_count": 19,
            "topics": ["flutter", "dart", "state-management", "riverpod", "bloc"],
            "created_at": "2025-01-07T14:00:00Z",
            "updated_at": "2025-01-28T14:00:00Z",
            "owner": {"login": "flutterdev", "avatar_url": "https://avatars.githubusercontent.com/u/13"}
        },
        {
            "id": 14,
            "name": "elixir-phoenix-liveview",
            "full_name": "elixirfan/elixir-phoenix-liveview",
            "description": "Real-time applications with Phoenix LiveView: examples, patterns, and production-ready templates.",
            "html_url": "https://github.com/elixirfan/elixir-phoenix-liveview",
            "stargazers_count": 2900,
            "language": "Elixir",
            "forks_count": 180,
            "open_issues_count": 8,
            "topics": ["elixir", "phoenix", "liveview", "real-time", "web"],
            "created_at": "2025-01-16T11:00:00Z",
            "updated_at": "2025-01-27T10:00:00Z",
            "owner": {"login": "elixirfan", "avatar_url": "https://avatars.githubusercontent.com/u/14"}
        },
        {
            "id": 15,
            "name": "django-saas-starter",
            "full_name": "djangodev/django-saas-starter",
            "description": "Complete Django SaaS starter with multi-tenancy, Stripe billing, teams, and admin dashboard.",
            "html_url": "https://github.com/djangodev/django-saas-starter",
            "stargazers_count": 7500,
            "language": "Python",
            "forks_count": 480,
            "open_issues_count": 36,
            "topics": ["django", "python", "saas", "stripe", "multitenancy"],
            "created_at": "2025-01-02T09:00:00Z",
            "updated_at": "2025-01-28T15:00:00Z",
            "owner": {"login": "djangodev", "avatar_url": "https://avatars.githubusercontent.com/u/15"}
        },
        {
            "id": 16,
            "name": "solidjs-components",
            "full_name": "solidfan/solidjs-components",
            "description": "Modern UI component library for SolidJS with accessibility, theming, and TypeScript support.",
            "html_url": "https://github.com/solidfan/solidjs-components",
            "stargazers_count": 2100,
            "language": "TypeScript",
            "forks_count": 95,
            "open_issues_count": 6,
            "topics": ["solidjs", "typescript", "ui", "components", "frontend"],
            "created_at": "2025-01-17T13:00:00Z",
            "updated_at": "2025-01-28T12:00:00Z",
            "owner": {"login": "solidfan", "avatar_url": "https://avatars.githubusercontent.com/u/16"}
        },
        {
            "id": 17,
            "name": "clojure-data-processing",
            "full_name": "clojurist/clojure-data-processing",
            "description": "High-performance data processing library in Clojure with functional transformations and parallel execution.",
            "html_url": "https://github.com/clojurist/clojure-data-processing",
            "stargazers_count": 1800,
            "language": "Clojure",
            "forks_count": 85,
            "open_issues_count": 4,
            "topics": ["clojure", "data-processing", "functional", "big-data"],
            "created_at": "2025-01-18T10:00:00Z",
            "updated_at": "2025-01-26T14:00:00Z",
            "owner": {"login": "clojurist", "avatar_url": "https://avatars.githubusercontent.com/u/17"}
        },
        {
            "id": 18,
            "name": "zig-systems-programming",
            "full_name": "zigfan/zig-systems-programming",
            "description": "Systems programming examples and tools in Zig: memory allocators, kernel modules, and embedded projects.",
            "html_url": "https://github.com/zigfan/zig-systems-programming",
            "stargazers_count": 3200,
            "language": "Zig",
            "forks_count": 220,
            "open_issues_count": 11,
            "topics": ["zig", "systems", "embedded", "kernel", "low-level"],
            "created_at": "2025-01-19T08:00:00Z",
            "updated_at": "2025-01-27T13:00:00Z",
            "owner": {"login": "zigfan", "avatar_url": "https://avatars.githubusercontent.com/u/18"}
        },
        {
            "id": 19,
            "name": "angular-architecture-patterns",
            "full_name": "ngdev/angular-architecture-patterns",
            "description": "Enterprise Angular architecture patterns: Nx monorepos, state management, testing, and performance.",
            "html_url": "https://github.com/ngdev/angular-architecture-patterns",
            "stargazers_count": 5800,
            "language": "TypeScript",
            "forks_count": 420,
            "open_issues_count": 24,
            "topics": ["angular", "typescript", "architecture", "nx", "enterprise"],
            "created_at": "2025-01-20T15:00:00Z",
            "updated_at": "2025-01-28T09:00:00Z",
            "owner": {"login": "ngdev", "avatar_url": "https://avatars.githubusercontent.com/u/19"}
        },
        {
            "id": 20,
            "name": "laravel-saas-boilerplate",
            "full_name": "laraveller/laravel-saas-boilerplate",
            "description": "Production-ready Laravel SaaS boilerplate with Jetstream, Cashier, teams, and API resources.",
            "html_url": "https://github.com/laraveller/laravel-saas-boilerplate",
            "stargazers_count": 4100,
            "language": "PHP",
            "forks_count": 310,
            "open_issues_count": 17,
            "topics": ["laravel", "php", "saas", "jetstream", "stripe"],
            "created_at": "2025-01-21T11:00:00Z",
            "updated_at": "2025-01-28T16:00:00Z",
            "owner": {"login": "laraveller", "avatar_url": "https://avatars.githubusercontent.com/u/20"}
        },
        {
            "id": 21,
            "name": "swiftui-components-library",
            "full_name": "swiftdev/swiftui-components-library",
            "description": "Beautiful SwiftUI component library with animations, custom controls, and iOS 17+ features.",
            "html_url": "https://github.com/swiftdev/swiftui-components-library",
            "stargazers_count": 3600,
            "language": "Swift",
            "forks_count": 190,
            "open_issues_count": 13,
            "topics": ["swift", "swiftui", "ios", "components", "ui"],
            "created_at": "2025-01-22T09:00:00Z",
            "updated_at": "2025-01-28T10:00:00Z",
            "owner": {"login": "swiftdev", "avatar_url": "https://avatars.githubusercontent.com/u/21"}
        },
        {
            "id": 22,
            "name": "kotlin-multiplatform-sdk",
            "full_name": "kotlindev/kotlin-multiplatform-sdk",
            "description": "Cross-platform SDK development with Kotlin Multiplatform: iOS, Android, Web, and Desktop support.",
            "html_url": "https://github.com/kotlindev/kotlin-multiplatform-sdk",
            "stargazers_count": 2700,
            "language": "Kotlin",
            "forks_count": 150,
            "open_issues_count": 9,
            "topics": ["kotlin", "multiplatform", "mobile", "android", "ios"],
            "created_at": "2025-01-23T14:00:00Z",
            "updated_at": "2025-01-27T11:00:00Z",
            "owner": {"login": "kotlindev", "avatar_url": "https://avatars.githubusercontent.com/u/22"}
        },
        {
            "id": 23,
            "name": "cpp-game-engine",
            "full_name": "gamedev/cpp-game-engine",
            "description": "Modern C++ game engine with Vulkan renderer, ECS architecture, and hot-reloading support.",
            "html_url": "https://github.com/gamedev/cpp-game-engine",
            "stargazers_count": 5200,
            "language": "C++",
            "forks_count": 380,
            "open_issues_count": 26,
            "topics": ["cpp", "game-engine", "vulkan", "ecs", "games"],
            "created_at": "2025-01-24T10:00:00Z",
            "updated_at": "2025-01-28T14:00:00Z",
            "owner": {"login": "gamedev", "avatar_url": "https://avatars.githubusercontent.com/u/23"}
        },
        {
            "id": 24,
            "name": "ruby-on-rails-api-template",
            "full_name": "rubyist/ruby-on-rails-api-template",
            "description": "Production-ready Rails API template with JWT auth, versioning, documentation, and testing setup.",
            "html_url": "https://github.com/rubyist/ruby-on-rails-api-template",
            "stargazers_count": 2400,
            "language": "Ruby",
            "forks_count": 140,
            "open_issues_count": 7,
            "topics": ["ruby", "rails", "api", "jwt", "backend"],
            "created_at": "2025-01-25T08:00:00Z",
            "updated_at": "2025-01-28T08:00:00Z",
            "owner": {"login": "rubyist", "avatar_url": "https://avatars.githubusercontent.com/u/24"}
        },
        {
            "id": 25,
            "name": "haskell-web-framework",
            "full_name": "haskeller/haskell-web-framework",
            "description": "Type-safe web framework in Haskell with servant-style routing and automatic API documentation.",
            "html_url": "https://github.com/haskeller/haskell-web-framework",
            "stargazers_count": 1500,
            "language": "Haskell",
            "forks_count": 75,
            "open_issues_count": 3,
            "topics": ["haskell", "web", "framework", "type-safe", "api"],
            "created_at": "2025-01-26T11:00:00Z",
            "updated_at": "2025-01-28T12:00:00Z",
            "owner": {"login": "haskeller", "avatar_url": "https://avatars.githubusercontent.com/u/25"}
        }
    ]
    return mock_repos

def get_language_color(language: str) -> str:
    """Get GitHub-like color for a programming language."""
    colors = {
        "Python": "#3572A5",
        "JavaScript": "#f1e05a",
        "TypeScript": "#2b7489",
        "Go": "#00ADD8",
        "Rust": "#dea584",
        "Java": "#b07219",
        "C++": "#f34b7d",
        "C": "#555555",
        "Ruby": "#701516",
        "PHP": "#4F5D95",
        "Swift": "#ffac45",
        "Kotlin": "#A97BFF",
        "C#": "#178600",
        "Vue": "#41b883",
        "Dart": "#00B4AB",
        "Elixir": "#6e4a7e",
        "Clojure": "#db5855",
        "Zig": "#ec915c",
        "Haskell": "#5e5086"
    }
    return colors.get(language, "#8b949e")

def format_number(num: int) -> str:
    """Format large numbers with k/m suffixes."""
    if num >= 1000000:
        return f"{num / 1000000:.1f}m"
    elif num >= 1000:
        return f"{num / 1000:.1f}k"
    return str(num)

def slugify(text: str) -> str:
    """Create URL-friendly slug from text."""
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def get_base_html(title: str, description: str, extra_head: str = "") -> str:
    """Get base HTML template with common styles."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <title>{title} | GitHub Trends</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #21262d;
            --border: #30363d;
            --text-primary: #f0f6fc;
            --text-secondary: #8b949e;
            --accent: #58a6ff;
            --accent-hover: #79c0ff;
            --success: #3fb950;
            --warning: #d29922;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        header {{
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border);
            padding: 20px 0;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        
        .header-content {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        
        .logo {{
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
            color: var(--text-primary);
        }}
        
        .logo-icon {{
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, var(--accent), #a371f7);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 18px;
        }}
        
        .logo-text {{
            font-size: 20px;
            font-weight: 700;
        }}
        
        .logo-text span {{
            color: var(--accent);
        }}
        
        nav {{
            display: flex;
            gap: 24px;
        }}
        
        nav a {{
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: color 0.2s;
        }}
        
        nav a:hover {{
            color: var(--text-primary);
        }}
        
        main {{
            padding: 40px 0;
        }}
        
        .hero {{
            text-align: center;
            padding: 60px 0;
            background: linear-gradient(180deg, rgba(88, 166, 255, 0.1) 0%, transparent 100%);
            border-bottom: 1px solid var(--border);
            margin-bottom: 40px;
        }}
        
        .hero h1 {{
            font-size: 48px;
            font-weight: 700;
            margin-bottom: 16px;
            background: linear-gradient(135deg, var(--text-primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .hero p {{
            font-size: 18px;
            color: var(--text-secondary);
            max-width: 600px;
            margin: 0 auto;
        }}
        
        .stats-bar {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 32px;
        }}
        
        .stat {{
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 32px;
            font-weight: 700;
            color: var(--accent);
        }}
        
        .stat-label {{
            font-size: 13px;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .section-title {{
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .repo-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .repo-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
            text-decoration: none;
            color: inherit;
            display: block;
        }}
        
        .repo-card:hover {{
            transform: translateY(-2px);
            border-color: var(--accent);
            box-shadow: 0 8px 24px rgba(88, 166, 255, 0.15);
        }}
        
        .repo-header {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            margin-bottom: 12px;
        }}
        
        .repo-name {{
            font-size: 16px;
            font-weight: 600;
            color: var(--accent);
            word-break: break-word;
        }}
        
        .repo-stars {{
            display: flex;
            align-items: center;
            gap: 4px;
            font-size: 14px;
            font-weight: 500;
            color: var(--text-secondary);
            flex-shrink: 0;
            margin-left: 8px;
        }}
        
        .repo-stars svg {{
            width: 16px;
            height: 16px;
            fill: var(--warning);
        }}
        
        .repo-desc {{
            font-size: 14px;
            color: var(--text-secondary);
            line-height: 1.5;
            margin-bottom: 16px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .repo-footer {{
            display: flex;
            align-items: center;
            gap: 16px;
            font-size: 13px;
            color: var(--text-secondary);
        }}
        
        .repo-lang {{
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        
        .lang-color {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }}
        
        .repo-forks, .repo-issues {{
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        
        .category-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 40px;
        }}
        
        .category-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 20px;
            text-decoration: none;
            color: inherit;
            transition: all 0.2s;
            text-align: center;
        }}
        
        .category-card:hover {{
            background: var(--bg-tertiary);
            border-color: var(--accent);
        }}
        
        .category-icon {{
            font-size: 32px;
            margin-bottom: 8px;
        }}
        
        .category-name {{
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 4px;
        }}
        
        .category-count {{
            font-size: 13px;
            color: var(--text-secondary);
        }}
        
        .topics {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: 12px;
        }}
        
        .topic {{
            background: var(--bg-tertiary);
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            color: var(--accent);
        }}
        
        .breadcrumb {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 24px;
            font-size: 14px;
        }}
        
        .breadcrumb a {{
            color: var(--accent);
            text-decoration: none;
        }}
        
        .breadcrumb a:hover {{
            text-decoration: underline;
        }}
        
        .breadcrumb-sep {{
            color: var(--text-secondary);
        }}
        
        .breadcrumb-current {{
            color: var(--text-secondary);
        }}
        
        .repo-detail {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 32px;
        }}
        
        .repo-detail-header {{
            display: flex;
            align-items: flex-start;
            gap: 20px;
            margin-bottom: 24px;
            padding-bottom: 24px;
            border-bottom: 1px solid var(--border);
        }}
        
        .repo-avatar {{
            width: 64px;
            height: 64px;
            border-radius: 12px;
        }}
        
        .repo-detail-info {{
            flex: 1;
        }}
        
        .repo-detail-title {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        
        .repo-detail-desc {{
            font-size: 16px;
            color: var(--text-secondary);
        }}
        
        .repo-detail-stats {{
            display: flex;
            gap: 24px;
            margin-top: 20px;
        }}
        
        .detail-stat {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 12px 20px;
            background: var(--bg-tertiary);
            border-radius: 8px;
        }}
        
        .detail-stat-value {{
            font-size: 20px;
            font-weight: 700;
        }}
        
        .detail-stat-label {{
            font-size: 13px;
            color: var(--text-secondary);
        }}
        
        .cta-button {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: var(--success);
            color: var(--bg-primary);
            padding: 12px 24px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            transition: opacity 0.2s;
        }}
        
        .cta-button:hover {{
            opacity: 0.9;
        }}
        
        footer {{
            background: var(--bg-secondary);
            border-top: 1px solid var(--border);
            padding: 40px 0;
            margin-top: 60px;
            text-align: center;
        }}
        
        footer p {{
            color: var(--text-secondary);
            font-size: 14px;
        }}
        
        .alternatives {{
            margin-top: 40px;
        }}
        
        .alternatives h3 {{
            font-size: 18px;
            margin-bottom: 16px;
        }}
        
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 32px;
            }}
            
            .repo-grid {{
                grid-template-columns: 1fr;
            }}
            
            .repo-detail-header {{
                flex-direction: column;
                text-align: center;
            }}
            
            .repo-detail-stats {{
                flex-wrap: wrap;
                justify-content: center;
            }}
            
            .stats-bar {{
                flex-direction: column;
                gap: 20px;
            }}
            
            nav {{
                display: none;
            }}
        }}
    </style>
    {extra_head}
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <a href="index.html" class="logo">
                    <div class="logo-icon">GT</div>
                    <div class="logo-text">GitHub<span>Trends</span></div>
                </a>
                <nav>
                    <a href="index.html">Trending</a>
                    <a href="categories/index.html">Languages</a>
                    <a href="#categories">Categories</a>
                </nav>
            </div>
        </div>
    </header>
    <main>
        <div class="container">
'''

def get_footer_html() -> str:
    """Get footer HTML."""
    return '''
        </div>
    </main>
    <footer>
        <div class="container">
            <p>Generated by GitHub Trends Analyzer • Data updated daily • Not affiliated with GitHub</p>
        </div>
    </footer>
</body>
</html>
'''

def generate_index_page(repos: List[Dict], language_stats: Dict) -> str:
    """Generate the main index page."""
    html = get_base_html(
        "Trending Repositories",
        "Discover trending GitHub repositories across all programming languages. Updated daily with the most starred projects."
    )
    
    total_stars = sum(r.get("stargazers_count", 0) for r in repos)
    total_forks = sum(r.get("forks_count", 0) for r in repos)
    
    html += f'''
    <section class="hero">
        <h1>GitHub Trends</h1>
        <p>Discover the most exciting open source projects trending on GitHub right now</p>
        <div class="stats-bar">
            <div class="stat">
                <div class="stat-value">{format_number(len(repos))}</div>
                <div class="stat-label">Repositories</div>
            </div>
            <div class="stat">
                <div class="stat-value">{format_number(total_stars)}</div>
                <div class="stat-label">Total Stars</div>
            </div>
            <div class="stat">
                <div class="stat-value">{format_number(total_forks)}</div>
                <div class="stat-label">Total Forks</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len(language_stats)}</div>
                <div class="stat-label">Languages</div>
            </div>
        </div>
    </section>
    
    <section id="categories">
        <h2 class="section-title">
            <span>📊</span> Browse by Language
        </h2>
        <div class="category-grid">
'''
    
    # Language icons/emoji mapping
    lang_icons = {
        "Python": "🐍",
        "JavaScript": "🟨",
        "TypeScript": "📘",
        "Go": "🐹",
        "Rust": "🦀",
        "Java": "☕",
        "C++": "⚡",
        "Ruby": "💎",
        "PHP": "🐘",
        "Swift": "🐦",
        "Kotlin": "🎯",
        "Vue": "🟩",
        "Dart": "🎯",
        "Elixir": "💧",
        "Clojure": "🔷",
        "Zig": "⚡",
        "Haskell": "🌊",
        "C": "🔧"
    }
    
    for lang, count in sorted(language_stats.items(), key=lambda x: x[1], reverse=True):
        icon = lang_icons.get(lang, "📦")
        slug = slugify(lang)
        html += f'''
            <a href="categories/{slug}.html" class="category-card">
                <div class="category-icon">{icon}</div>
                <div class="category-name">{lang}</div>
                <div class="category-count">{count} repos</div>
            </a>
'''
    
    html += '''
        </div>
    </section>
    
    <section id="trending">
        <h2 class="section-title">
            <span>🔥</span> Trending Now
        </h2>
        <div class="repo-grid">
'''
    
    for repo in repos[:20]:
        lang = repo.get("language") or "Unknown"
        color = get_language_color(lang)
        slug = slugify(repo["full_name"])
        
        topics_html = ""
        topics = repo.get("topics", [])
        if topics:
            topics_html = '<div class="topics">' + ''.join([
                f'<span class="topic">{t}</span>' for t in topics[:4]
            ]) + '</div>'
        
        html += f'''
            <a href="repos/{slug}.html" class="repo-card">
                <div class="repo-header">
                    <span class="repo-name">{repo["full_name"]}</span>
                    <span class="repo-stars">
                        <svg viewBox="0 0 16 16"><path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"/></svg>
                        {format_number(repo.get("stargazers_count", 0))}
                    </span>
                </div>
                <p class="repo-desc">{repo.get("description") or "No description available"}</p>
                <div class="repo-footer">
                    <span class="repo-lang">
                        <span class="lang-color" style="background: {color};"></span>
                        {lang}
                    </span>
                    <span class="repo-forks">⑂ {format_number(repo.get("forks_count", 0))}</span>
                    <span class="repo-issues">⊙ {format_number(repo.get("open_issues_count", 0))}</span>
                </div>
                {topics_html}
            </a>
'''
    
    html += '''
        </div>
    </section>
    '''
    
    html += get_footer_html()
    return html

def generate_category_page(lang: str, repos: List[Dict], all_languages: List[str]) -> str:
    """Generate a category page for a specific language."""
    lang_repos = [r for r in repos if r.get("language") == lang]
    lang_repos.sort(key=lambda x: x.get("stargazers_count", 0), reverse=True)
    
    color = get_language_color(lang)
    
    html = get_base_html(
        f"Top {lang} Repositories",
        f"Discover the most popular {lang} repositories on GitHub. Browse {len(lang_repos)} trending projects."
    )
    
    html += f'''
    <nav class="breadcrumb">
        <a href="../index.html">Home</a>
        <span class="breadcrumb-sep">›</span>
        <a href="index.html">Languages</a>
        <span class="breadcrumb-sep">›</span>
        <span class="breadcrumb-current">{lang}</span>
    </nav>
    
    <section class="hero" style="padding: 40px 0;">
        <h1>
            <span class="lang-color" style="background: {color}; display: inline-block; width: 24px; height: 24px; border-radius: 50%; vertical-align: middle; margin-right: 12px;"></span>
            Top {lang} Repositories
        </h1>
        <p>{len(lang_repos)} trending repositories • Updated daily</p>
    </section>
    
    <section>
        <div class="repo-grid">
'''
    
    for repo in lang_repos:
        slug = slugify(repo["full_name"])
        
        topics_html = ""
        topics = repo.get("topics", [])
        if topics:
            topics_html = '<div class="topics">' + ''.join([
                f'<span class="topic">{t}</span>' for t in topics[:4]
            ]) + '</div>'
        
        html += f'''
            <a href="../repos/{slug}.html" class="repo-card">
                <div class="repo-header">
                    <span class="repo-name">{repo["full_name"]}</span>
                    <span class="repo-stars">
                        <svg viewBox="0 0 16 16"><path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"/></svg>
                        {format_number(repo.get("stargazers_count", 0))}
                    </span>
                </div>
                <p class="repo-desc">{repo.get("description") or "No description available"}</p>
                <div class="repo-footer">
                    <span class="repo-lang">
                        <span class="lang-color" style="background: {color};"></span>
                        {lang}
                    </span>
                    <span class="repo-forks">⑂ {format_number(repo.get("forks_count", 0))}</span>
                    <span class="repo-issues">⊙ {format_number(repo.get("open_issues_count", 0))}</span>
                </div>
                {topics_html}
            </a>
'''
    
    html += '''
        </div>
    </section>
    '''
    
    html += get_footer_html()
    return html

def generate_repo_page(repo: Dict, all_repos: List[Dict]) -> str:
    """Generate individual repository detail page."""
    lang = repo.get("language") or "Unknown"
    color = get_language_color(lang)
    slug = slugify(repo["full_name"])
    lang_slug = slugify(lang)
    
    # Find similar repos (same language)
    similar_repos = [r for r in all_repos if r.get("language") == lang and r["id"] != repo["id"]]
    similar_repos.sort(key=lambda x: x.get("stargazers_count", 0), reverse=True)
    
    html = get_base_html(
        repo["full_name"],
        f"{repo.get('description', '')} • {format_number(repo.get('stargazers_count', 0))} stars • {lang} • GitHub repository details"
    )
    
    created_date = repo.get("created_at", "")[:10]
    updated_date = repo.get("updated_at", "")[:10]
    
    topics_html = ""
    topics = repo.get("topics", [])
    if topics:
        topics_html = '<div class="topics" style="margin-top: 16px;">' + ''.join([
            f'<span class="topic">{t}</span>' for t in topics
        ]) + '</div>'
    
    html += f'''
    <nav class="breadcrumb">
        <a href="../index.html">Home</a>
        <span class="breadcrumb-sep">›</span>
        <a href="../categories/{lang_slug}.html">{lang}</a>
        <span class="breadcrumb-sep">›</span>
        <span class="breadcrumb-current">{repo["name"]}</span>
    </nav>
    
    <article class="repo-detail">
        <div class="repo-detail-header">
            <img src="{repo["owner"]["avatar_url"]}" alt="{repo["owner"]["login"]}" class="repo-avatar">
            <div class="repo-detail-info">
                <h1 class="repo-detail-title">{repo["full_name"]}</h1>
                <p class="repo-detail-desc">{repo.get("description") or "No description available"}</p>
                {topics_html}
            </div>
        </div>
        
        <div class="repo-detail-stats">
            <div class="detail-stat">
                <span class="detail-stat-value" style="color: var(--warning);">⭐ {format_number(repo.get("stargazers_count", 0))}</span>
                <span class="detail-stat-label">Stars</span>
            </div>
            <div class="detail-stat">
                <span class="detail-stat-value">⑂ {format_number(repo.get("forks_count", 0))}</span>
                <span class="detail-stat-label">Forks</span>
            </div>
            <div class="detail-stat">
                <span class="detail-stat-value">⊙ {format_number(repo.get("open_issues_count", 0))}</span>
                <span class="detail-stat-label">Open Issues</span>
            </div>
            <div class="detail-stat">
                <span class="detail-stat-value">
                    <span class="lang-color" style="background: {color}; display: inline-block; width: 12px; height: 12px; border-radius: 50%;"></span>
                    {lang}
                </span>
                <span class="detail-stat-label">Language</span>
            </div>
        </div>
        
        <div style="margin-top: 24px; padding-top: 24px; border-top: 1px solid var(--border);">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; color: var(--text-secondary); font-size: 14px;">
                <div>
                    <strong style="color: var(--text-primary);">Created</strong><br>
                    {created_date}
                </div>
                <div>
                    <strong style="color: var(--text-primary);">Last Updated</strong><br>
                    {updated_date}
                </div>
                <div>
                    <strong style="color: var(--text-primary);">Owner</strong><br>
                    @{repo["owner"]["login"]}
                </div>
            </div>
        </div>
        
        <div style="margin-top: 32px;">
            <a href="{repo["html_url"]}" class="cta-button" target="_blank" rel="noopener">
                View on GitHub →
            </a>
        </div>
    </article>
'''
    
    # Add similar repos section
    if similar_repos:
        html += '''
    <section class="alternatives">
        <h3>Similar Repositories</h3>
        <div class="repo-grid">
'''
        for similar in similar_repos[:4]:
            similar_slug = slugify(similar["full_name"])
            similar_lang = similar.get("language") or "Unknown"
            similar_color = get_language_color(similar_lang)
            
            html += f'''
            <a href="{similar_slug}.html" class="repo-card">
                <div class="repo-header">
                    <span class="repo-name">{similar["full_name"]}</span>
                    <span class="repo-stars">
                        <svg viewBox="0 0 16 16"><path d="M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"/></svg>
                        {format_number(similar.get("stargazers_count", 0))}
                    </span>
                </div>
                <p class="repo-desc">{similar.get("description") or "No description"}</p>
                <div class="repo-footer">
                    <span class="repo-lang">
                        <span class="lang-color" style="background: {similar_color};"></span>
                        {similar_lang}
                    </span>
                </div>
            </a>
'''
        html += '''
        </div>
    </section>
'''
    
    html += get_footer_html()
    return html

def generate_categories_index_page(languages: List[str], language_stats: Dict, repos: List[Dict]) -> str:
    """Generate the categories index page."""
    html = get_base_html(
        "Browse by Language",
        "Explore trending GitHub repositories by programming language. Find the best projects in Python, TypeScript, Rust, Go, and more."
    )
    
    # Language descriptions
    lang_desc = {
        "Python": "Machine learning, web frameworks, and automation tools",
        "JavaScript": "Frontend frameworks, Node.js tools, and web applications",
        "TypeScript": "Type-safe JavaScript for large-scale applications",
        "Go": "Cloud-native tools, microservices, and CLI applications",
        "Rust": "Systems programming, WebAssembly, and high-performance tools",
        "C++": "Game engines, system software, and performance-critical apps",
        "Java": "Enterprise applications, Android development, and backends",
        "Ruby": "Web development with Rails and developer tooling",
        "PHP": "Web applications, Laravel frameworks, and CMS platforms",
        "Swift": "iOS, macOS apps, and system programming",
        "Kotlin": "Android development and multiplatform applications",
        "Vue": "Progressive frontend framework for modern web apps",
        "Dart": "Flutter cross-platform mobile development",
        "Elixir": "Scalable real-time applications with Phoenix",
        "Clojure": "Functional programming on the JVM",
        "Zig": "Modern systems programming with C interop",
        "Haskell": "Purely functional programming and type safety",
        "C": "Operating systems, embedded systems, and low-level tools"
    }
    
    # Language icons
    lang_icons = {
        "Python": "🐍", "JavaScript": "🟨", "TypeScript": "📘", "Go": "🐹",
        "Rust": "🦀", "Java": "☕", "C++": "⚡", "Ruby": "💎",
        "PHP": "🐘", "Swift": "🐦", "Kotlin": "🎯", "Vue": "🟩",
        "Dart": "🎯", "Elixir": "💧", "Clojure": "🔷", "Zig": "⚡",
        "Haskell": "🌊", "C": "🔧"
    }
    
    html += '''
    <nav class="breadcrumb">
        <a href="../index.html">Home</a>
        <span class="breadcrumb-sep">›</span>
        <span class="breadcrumb-current">Languages</span>
    </nav>
    
    <section class="hero" style="padding: 40px 0;">
        <h1>Browse by Language</h1>
        <p>Find trending repositories in your favorite programming language</p>
    </section>
    
    <section>
        <div class="repo-grid">
'''
    
    for lang in sorted(languages):
        count = language_stats.get(lang, 0)
        desc = lang_desc.get(lang, f"Popular {lang} projects")
        icon = lang_icons.get(lang, "📦")
        slug = slugify(lang)
        color = get_language_color(lang)
        
        # Get top repo for this language
        lang_repos = [r for r in repos if r.get("language") == lang]
        top_repo = max(lang_repos, key=lambda x: x.get("stargazers_count", 0)) if lang_repos else None
        top_stars = format_number(top_repo.get("stargazers_count", 0)) if top_repo else "0"
        
        html += f'''
            <a href="{slug}.html" class="repo-card">
                <div class="repo-header">
                    <span class="repo-name">{icon} {lang}</span>
                    <span class="repo-stars">{count} repos</span>
                </div>
                <p class="repo-desc">{desc}</p>
                <div class="repo-footer">
                    <span class="repo-lang">
                        <span class="lang-color" style="background: {color};"></span>
                        Top: {top_stars} ⭐
                    </span>
                </div>
            </a>
'''
    
    html += '''
        </div>
    </section>
    '''
    
    html += get_footer_html()
    return html

def generate_sitemap(base_url: str, repos: List[Dict], languages: List[str]) -> str:
    """Generate sitemap.xml for SEO."""
    now = datetime.now().strftime("%Y-%m-%d")
    
    urls = [
        f"  <url>\n    <loc>{base_url}/index.html</loc>\n    <lastmod>{now}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>1.0</priority>\n  </url>",
        f"  <url>\n    <loc>{base_url}/categories/index.html</loc>\n    <lastmod>{now}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>0.9</priority>\n  </url>"
    ]
    
    for lang in languages:
        slug = slugify(lang)
        urls.append(f"  <url>\n    <loc>{base_url}/categories/{slug}.html</loc>\n    <lastmod>{now}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>0.8</priority>\n  </url>")
    
    for repo in repos:
        slug = slugify(repo["full_name"])
        urls.append(f"  <url>\n    <loc>{base_url}/repos/{slug}.html</loc>\n    <lastmod>{now}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.7</priority>\n  </url>")
    
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>'

def main():
    """Main function to generate all static pages."""
    print("🚀 GitHub Trends Analyzer MVP")
    print("=" * 40)
    
    ensure_dirs()
    
    # Fetch data
    print("\n📥 Fetching trending repositories...")
    repos = fetch_trending_repos()
    print(f"✅ Loaded {len(repos)} repositories")
    
    # Calculate language stats
    language_stats = {}
    for repo in repos:
        lang = repo.get("language") or "Unknown"
        language_stats[lang] = language_stats.get(lang, 0) + 1
    
    languages = list(language_stats.keys())
    
    # Generate index page
    print("\n📝 Generating pages...")
    index_html = generate_index_page(repos, language_stats)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print("  ✓ index.html")
    
    # Generate category pages
    categories_index = generate_categories_index_page(languages, language_stats, repos)
    with open(os.path.join(CATEGORIES_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(categories_index)
    print("  ✓ categories/index.html")
    
    for lang in languages:
        slug = slugify(lang)
        cat_html = generate_category_page(lang, repos, languages)
        with open(os.path.join(CATEGORIES_DIR, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(cat_html)
        print(f"  ✓ categories/{slug}.html")
    
    # Generate repo pages
    for repo in repos:
        slug = slugify(repo["full_name"])
        repo_html = generate_repo_page(repo, repos)
        with open(os.path.join(REPOS_DIR, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(repo_html)
        print(f"  ✓ repos/{slug}.html")
    
    # Generate sitemap
    sitemap = generate_sitemap("https://yourusername.github.io/github-trends", repos, languages)
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    print("  ✓ sitemap.xml")
    
    # Generate stats
    total_pages = 1 + 1 + len(languages) + len(repos)
    
    print("\n" + "=" * 40)
    print("✅ Generation Complete!")
    print(f"\n📊 Statistics:")
    print(f"   • Repositories: {len(repos)}")
    print(f"   • Languages: {len(languages)}")
    print(f"   • Total pages: {total_pages}")
    print(f"\n📁 Output directory: {OUTPUT_DIR}/")
    print("\n🚀 Ready for deployment to GitHub Pages!")

if __name__ == "__main__":
    main()
