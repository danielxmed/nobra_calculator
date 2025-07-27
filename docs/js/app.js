// nobra_calculator Interactive Documentation
// Main application logic

class NobraCalculatorDocs {
    constructor() {
        this.apiBaseUrl = window.location.origin;
        this.scores = [];
        this.categories = new Set();
        this.calculationsToday = 0;
        this.responseTimes = [];
        
        this.init();
    }

    async init() {
        try {
            await this.loadScores();
            this.setupEventListeners();
            this.updateStatistics();
            this.checkApiStatus();
        } catch (error) {
            console.error('Failed to initialize application:', error);
            this.showError('Failed to load application. Please refresh the page.');
        }
    }

    async loadScores() {
        const startTime = performance.now();
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/scores`);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            
            const data = await response.json();
            this.scores = data.scores || [];
            
            // Extract categories
            this.scores.forEach(score => {
                if (score.category) {
                    this.categories.add(score.category);
                }
            });
            
            // Record response time
            const responseTime = performance.now() - startTime;
            this.responseTimes.push(responseTime);
            
            this.renderScores();
            this.populateCategoryFilter();
            this.hideLoading();
            
        } catch (error) {
            console.error('Failed to load scores:', error);
            this.showError('Failed to load medical scores. Please check your connection.');
        }
    }

    renderScores(filteredScores = null) {
        const container = document.getElementById('scores-container');
        const scoresToRender = filteredScores || this.scores;
        
        if (scoresToRender.length === 0) {
            this.showEmptyState();
            return;
        }
        
        this.hideEmptyState();
        
        container.innerHTML = scoresToRender.map(score => `
            <div class="score-card bg-white rounded-lg shadow-md p-6 cursor-pointer" 
                 data-score-id="${score.id}">
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-lg font-semibold text-gray-900 leading-tight">
                        ${score.title}
                    </h3>
                    <span class="category-badge category-${score.category}">
                        ${this.formatCategory(score.category)}
                    </span>
                </div>
                
                <p class="text-gray-600 text-sm mb-4 line-clamp-3">
                    ${score.description}
                </p>
                
                <div class="flex justify-between items-center">
                    <span class="text-xs text-gray-500">
                        Version: ${score.version || 'Standard'}
                    </span>
                    <button class="text-blue-600 hover:text-blue-800 text-sm font-medium">
                        View Details →
                    </button>
                </div>
            </div>
        `).join('');
        
        // Add click listeners
        container.querySelectorAll('.score-card').forEach(card => {
            card.addEventListener('click', (e) => {
                const scoreId = card.dataset.scoreId;
                this.showScoreDetail(scoreId);
            });
        });
    }

    async showScoreDetail(scoreId) {
        try {
            const startTime = performance.now();
            const response = await fetch(`${this.apiBaseUrl}/api/scores/${scoreId}`);
            
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            
            const scoreData = await response.json();
            const responseTime = performance.now() - startTime;
            this.responseTimes.push(responseTime);
            
            this.renderScoreModal(scoreData);
            this.showModal();
            
        } catch (error) {
            console.error('Failed to load score details:', error);
            this.showError(`Failed to load details for ${scoreId}`);
        }
    }

    renderScoreModal(score) {
        const modalContent = document.getElementById('modal-content');
        
        modalContent.innerHTML = `
            <!-- Modal Header -->
            <div class="flex justify-between items-start p-6 border-b">
                <div>
                    <h2 class="text-2xl font-bold text-gray-900">${score.title}</h2>
                    <div class="flex items-center gap-2 mt-2">
                        <span class="category-badge category-${score.category}">
                            ${this.formatCategory(score.category)}
                        </span>
                        <span class="text-sm text-gray-500">Version: ${score.version || 'Standard'}</span>
                    </div>
                </div>
                <button id="close-modal" class="text-gray-400 hover:text-gray-600">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
            
            <!-- Modal Body -->
            <div class="p-6">
                <!-- Description -->
                <div class="mb-8">
                    <h3 class="text-lg font-semibold mb-3">Description</h3>
                    <p class="text-gray-700 leading-relaxed">${score.description}</p>
                </div>
                
                <!-- Formula -->
                ${score.formula ? `
                <div class="mb-8">
                    <h3 class="text-lg font-semibold mb-3">Formula</h3>
                    <div class="bg-gray-100 p-4 rounded-lg">
                        <code class="text-sm">${score.formula}</code>
                    </div>
                </div>
                ` : ''}
                
                <!-- Parameters -->
                <div class="mb-8">
                    <h3 class="text-lg font-semibold mb-4">Parameters</h3>
                    <div class="space-y-4">
                        ${score.parameters.map(param => this.renderParameter(param)).join('')}
                    </div>
                </div>
                
                <!-- Calculator -->
                <div class="mb-8">
                    <h3 class="text-lg font-semibold mb-4">Interactive Calculator</h3>
                    <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
                        <form id="calculator-form" data-score-id="${score.id}">
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                                ${score.parameters.map(param => this.renderCalculatorInput(param)).join('')}
                            </div>
                            <button type="submit" class="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors">
                                Calculate ${score.title}
                            </button>
                        </form>
                        
                        <!-- Result Display -->
                        <div id="calculation-result" class="hidden mt-6">
                            <!-- Result will be displayed here -->
                        </div>
                    </div>
                </div>
                
                <!-- Interpretation Ranges -->
                ${score.interpretation && score.interpretation.ranges ? `
                <div class="mb-8">
                    <h3 class="text-lg font-semibold mb-4">Result Interpretation</h3>
                    <div class="space-y-3">
                        ${score.interpretation.ranges.map(range => this.renderInterpretationRange(range)).join('')}
                    </div>
                </div>
                ` : ''}
                
                <!-- Notes -->
                ${score.notes && score.notes.length > 0 ? `
                <div class="mb-8">
                    <h3 class="text-lg font-semibold mb-3">Important Notes</h3>
                    <ul class="list-disc list-inside space-y-2 text-gray-700">
                        ${score.notes.map(note => `<li>${note}</li>`).join('')}
                    </ul>
                </div>
                ` : ''}
                
                <!-- References -->
                ${score.references && score.references.length > 0 ? `
                <div class="mb-6">
                    <h3 class="text-lg font-semibold mb-3">References</h3>
                    <ol class="list-decimal list-inside space-y-2 text-sm text-gray-700">
                        ${score.references.map(ref => `<li>${ref}</li>`).join('')}
                    </ol>
                </div>
                ` : ''}
            </div>
        `;
        
        // Setup modal event listeners
        this.setupModalEventListeners(score);
    }

    renderParameter(param) {
        const validationInfo = this.getValidationInfo(param);
        
        return `
            <div class="border border-gray-200 rounded-lg p-4">
                <div class="flex justify-between items-start mb-2">
                    <h4 class="font-medium text-gray-900">${param.name}</h4>
                    <span class="text-xs px-2 py-1 bg-gray-100 rounded">
                        ${param.type}${param.required ? ' *' : ''}
                    </span>
                </div>
                <p class="text-sm text-gray-600 mb-2">${param.description}</p>
                ${param.unit ? `<p class="text-xs text-gray-500 mb-2">Unit: ${param.unit}</p>` : ''}
                ${validationInfo ? `<div class="text-xs text-blue-600">${validationInfo}</div>` : ''}
                ${param.options ? `
                <div class="mt-2">
                    <span class="text-xs font-medium text-gray-700">Options:</span>
                    <div class="flex flex-wrap gap-1 mt-1">
                        ${param.options.map(opt => `
                            <span class="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded">${opt}</span>
                        `).join('')}
                    </div>
                </div>
                ` : ''}
            </div>
        `;
    }

    renderCalculatorInput(param) {
        if (param.options) {
            return `
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                        ${param.name}${param.required ? ' *' : ''}
                    </label>
                    <select name="${param.name}" ${param.required ? 'required' : ''} 
                            class="parameter-input w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none">
                        <option value="">Select ${param.name}</option>
                        ${param.options.map(opt => `<option value="${opt}">${opt}</option>`).join('')}
                    </select>
                </div>
            `;
        } else {
            const inputType = param.type === 'integer' || param.type === 'float' ? 'number' : 'text';
            const step = param.type === 'float' ? '0.01' : '1';
            const min = param.validation?.min || '';
            const max = param.validation?.max || '';
            
            return `
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">
                        ${param.name}${param.required ? ' *' : ''}
                        ${param.unit ? `(${param.unit})` : ''}
                    </label>
                    <input type="${inputType}" name="${param.name}" 
                           ${param.required ? 'required' : ''}
                           ${min ? `min="${min}"` : ''}
                           ${max ? `max="${max}"` : ''}
                           ${inputType === 'number' ? `step="${step}"` : ''}
                           placeholder="Enter ${param.name}"
                           class="parameter-input w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none">
                </div>
            `;
        }
    }

    renderInterpretationRange(range) {
        const severityClass = this.getSeverityClass(range.stage);
        const rangeText = this.formatRange(range.min, range.max);
        
        return `
            <div class="interpretation-range ${severityClass} bg-white border border-gray-200 rounded-lg p-4">
                <div class="flex justify-between items-start mb-2">
                    <span class="font-medium text-gray-900">${range.stage}</span>
                    <span class="text-sm text-gray-600">${rangeText}</span>
                </div>
                <p class="text-sm text-gray-700 mb-2">${range.description}</p>
                <p class="text-sm text-gray-600">${range.interpretation}</p>
            </div>
        `;
    }

    setupModalEventListeners(score) {
        // Close modal
        document.getElementById('close-modal').addEventListener('click', () => {
            this.hideModal();
        });
        
        // Calculator form
        const form = document.getElementById('calculator-form');
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.performCalculation(score.id, form);
        });
        
        // Close modal on backdrop click
        document.getElementById('score-modal').addEventListener('click', (e) => {
            if (e.target.id === 'score-modal') {
                this.hideModal();
            }
        });
    }

    async performCalculation(scoreId, form) {
        const formData = new FormData(form);
        const parameters = {};
        
        // Convert form data to appropriate types
        for (const [key, value] of formData.entries()) {
            if (value.trim() === '') continue;
            
            const param = this.getParameterByName(scoreId, key);
            if (param) {
                if (param.type === 'integer') {
                    parameters[key] = parseInt(value);
                } else if (param.type === 'float') {
                    parameters[key] = parseFloat(value);
                } else {
                    parameters[key] = value;
                }
            }
        }
        
        try {
            const startTime = performance.now();
            const response = await fetch(`${this.apiBaseUrl}/api/${scoreId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(parameters)
            });
            
            const responseTime = performance.now() - startTime;
            this.responseTimes.push(responseTime);
            this.calculationsToday++;
            this.updateStatistics();
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail?.message || `HTTP ${response.status}`);
            }
            
            const result = await response.json();
            this.displayCalculationResult(result);
            
        } catch (error) {
            console.error('Calculation failed:', error);
            this.displayCalculationError(error.message);
        }
    }

    displayCalculationResult(result) {
        const resultContainer = document.getElementById('calculation-result');
        const severityClass = this.getResultSeverityClass(result.stage);
        
        resultContainer.innerHTML = `
            <div class="${severityClass} text-white rounded-lg p-4">
                <div class="flex justify-between items-start mb-3">
                    <h4 class="text-lg font-semibold">Calculation Result</h4>
                    <span class="text-sm opacity-90">✓ Success</span>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                    <div>
                        <div class="text-2xl font-bold">${result.result} ${result.unit}</div>
                        ${result.stage ? `<div class="text-sm opacity-90">Stage: ${result.stage}</div>` : ''}
                    </div>
                    <div>
                        ${result.stage_description ? `<div class="text-sm font-medium">${result.stage_description}</div>` : ''}
                    </div>
                </div>
                
                <div class="border-t border-white border-opacity-20 pt-3">
                    <h5 class="font-medium mb-2">Clinical Interpretation:</h5>
                    <p class="text-sm opacity-90">${result.interpretation}</p>
                </div>
            </div>
        `;
        
        resultContainer.classList.remove('hidden');
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    displayCalculationError(errorMessage) {
        const resultContainer = document.getElementById('calculation-result');
        
        resultContainer.innerHTML = `
            <div class="bg-red-500 text-white rounded-lg p-4">
                <div class="flex items-start">
                    <svg class="w-5 h-5 mr-2 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
                    </svg>
                    <div>
                        <h4 class="font-semibold">Calculation Error</h4>
                        <p class="text-sm mt-1">${errorMessage}</p>
                    </div>
                </div>
            </div>
        `;
        
        resultContainer.classList.remove('hidden');
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    setupEventListeners() {
        // Search functionality
        const searchInput = document.getElementById('search-input');
        searchInput.addEventListener('input', (e) => {
            this.filterScores(e.target.value, document.getElementById('category-filter').value);
        });
        
        // Category filter
        const categoryFilter = document.getElementById('category-filter');
        categoryFilter.addEventListener('change', (e) => {
            this.filterScores(document.getElementById('search-input').value, e.target.value);
        });
        
        // Reset filters
        document.getElementById('reset-filters').addEventListener('click', () => {
            document.getElementById('search-input').value = '';
            document.getElementById('category-filter').value = '';
            this.renderScores();
        });
    }

    filterScores(searchTerm, category) {
        let filtered = this.scores;
        
        if (searchTerm) {
            const term = searchTerm.toLowerCase();
            filtered = filtered.filter(score => 
                score.title.toLowerCase().includes(term) ||
                score.description.toLowerCase().includes(term) ||
                score.category.toLowerCase().includes(term)
            );
        }
        
        if (category) {
            filtered = filtered.filter(score => score.category === category);
        }
        
        this.renderScores(filtered);
    }

    populateCategoryFilter() {
        const select = document.getElementById('category-filter');
        const sortedCategories = Array.from(this.categories).sort();
        
        sortedCategories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = this.formatCategory(category);
            select.appendChild(option);
        });
    }

    updateStatistics() {
        document.getElementById('total-scores').textContent = this.scores.length;
        document.getElementById('total-categories').textContent = this.categories.size;
        document.getElementById('calculations-today').textContent = this.calculationsToday;
        
        if (this.responseTimes.length > 0) {
            const avgTime = this.responseTimes.reduce((a, b) => a + b, 0) / this.responseTimes.length;
            document.getElementById('avg-response-time').textContent = Math.round(avgTime);
        }
    }

    async checkApiStatus() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const statusElement = document.getElementById('api-status');
            
            if (response.ok) {
                statusElement.innerHTML = `
                    <div class="w-3 h-3 bg-green-500 rounded-full"></div>
                    <span class="text-sm text-gray-700">API Online</span>
                `;
            } else {
                throw new Error('API not responding');
            }
        } catch (error) {
            const statusElement = document.getElementById('api-status');
            statusElement.innerHTML = `
                <div class="w-3 h-3 bg-red-500 rounded-full"></div>
                <span class="text-sm text-gray-700">API Offline</span>
            `;
        }
    }

    // Utility methods
    formatCategory(category) {
        return category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    getValidationInfo(param) {
        if (!param.validation) return null;
        
        const parts = [];
        if (param.validation.min !== undefined) parts.push(`Min: ${param.validation.min}`);
        if (param.validation.max !== undefined) parts.push(`Max: ${param.validation.max}`);
        if (param.validation.enum) parts.push(`Options: ${param.validation.enum.join(', ')}`);
        
        return parts.join(', ');
    }

    getSeverityClass(stage) {
        if (!stage) return 'normal';
        
        const stageLower = stage.toLowerCase();
        if (stageLower.includes('normal') || stageLower.includes('g1') || stageLower.includes('low')) return 'normal';
        if (stageLower.includes('mild') || stageLower.includes('g2') || stageLower.includes('moderate')) return 'mild';
        if (stageLower.includes('severe') || stageLower.includes('g4') || stageLower.includes('g5') || stageLower.includes('high')) return 'severe';
        return 'moderate';
    }

    getResultSeverityClass(stage) {
        const severity = this.getSeverityClass(stage);
        switch (severity) {
            case 'normal': return 'result-success';
            case 'mild': return 'result-warning';
            case 'moderate': return 'result-warning';
            case 'severe': return 'result-danger';
            default: return 'result-success';
        }
    }

    formatRange(min, max) {
        if (min === null || min === undefined) return `≤ ${max}`;
        if (max === null || max === undefined) return `≥ ${min}`;
        return `${min} - ${max}`;
    }

    getParameterByName(scoreId, paramName) {
        const score = this.scores.find(s => s.id === scoreId);
        return score?.parameters?.find(p => p.name === paramName);
    }

    showModal() {
        document.getElementById('score-modal').classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }

    hideModal() {
        document.getElementById('score-modal').classList.add('hidden');
        document.body.style.overflow = 'auto';
    }

    showEmptyState() {
        document.getElementById('empty-state').classList.remove('hidden');
        document.getElementById('scores-container').innerHTML = '';
    }

    hideEmptyState() {
        document.getElementById('empty-state').classList.add('hidden');
    }

    hideLoading() {
        document.getElementById('loading-state').style.display = 'none';
    }

    showError(message) {
        // Simple error display - could be enhanced with a toast system
        alert(message);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new NobraCalculatorDocs();
});